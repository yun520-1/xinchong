# Flask Web Application — 心虫 (Xinchong)

import os
import yaml
import uuid
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from flask_cors import CORS

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.conversation import ConversationManager
from src.api_client import APIClient
from src.heartflow import HeartFlow


def load_config():
    # Navigate from src/web/app.py -> src -> project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(project_root, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    CORS(app)

    cfg = load_config()
    app.config["XINCHONG_CFG"] = cfg

    # Initialize core components
    conv_mgr = ConversationManager(
        storage_path=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "sessions"
        )
    )
    app.config["CONV_MGR"] = conv_mgr

    # Initialize API client
    api_cfg = cfg.get("api", {})
    try:
        api_client = APIClient(api_cfg)
        app.config["API_CLIENT"] = api_client
        app.config["API_READY"] = True
    except Exception as e:
        print(f"Warning: API client init failed: {e}")
        app.config["API_CLIENT"] = None
        app.config["API_READY"] = False

    # HeartFlow engine
    hf_cfg = cfg.get("heartflow", {})
    hf = HeartFlow(verbose=hf_cfg.get("verbose", False))
    app.config["HEARTFLOW"] = hf

    return app


app = create_app()


# ============================================================
# Routes
# ============================================================

@app.route("/")
def index():
    """Main chat page"""
    cfg = app.config["XINCHONG_CFG"]
    conv_mgr = app.config["CONV_MGR"]
    sessions = conv_mgr.list_sessions()
    current_session = None

    session_id = request.args.get("session")
    if session_id:
        current_session = conv_mgr.get_session(session_id)

    if not current_session:
        # Create or get first session
        if sessions:
            current_session = conv_mgr.get_session(sessions[0]["id"])
        else:
            current_session = conv_mgr.create_session(
                title="新对话",
                system_prompt=cfg.get("conversation", {}).get("system_prompt", "")
            )

    return render_template(
        "index.html",
        session=current_session,
        sessions=sessions,
        cfg=cfg,
        api_ready=app.config.get("API_READY", False),
    )


@app.route("/api/sessions", methods=["GET"])
def list_sessions():
    """List all sessions"""
    conv_mgr = app.config["CONV_MGR"]
    return jsonify(conv_mgr.list_sessions())


@app.route("/api/sessions", methods=["POST"])
def create_session():
    """Create a new session"""
    conv_mgr = app.config["CONV_MGR"]
    cfg = app.config["XINCHONG_CFG"]
    data = request.get_json() or {}
    title = data.get("title", "新对话")
    system_prompt = cfg.get("conversation", {}).get("system_prompt", "")
    session = conv_mgr.create_session(title=title, system_prompt=system_prompt)
    return jsonify(session.to_dict())


@app.route("/api/sessions/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    """Delete a session"""
    conv_mgr = app.config["CONV_MGR"]
    conv_mgr.delete_session(session_id)
    return jsonify({"ok": True})


@app.route("/api/sessions/<session_id>/messages", methods=["GET"])
def get_messages(session_id):
    """Get messages for a session"""
    conv_mgr = app.config["CONV_MGR"]
    messages = conv_mgr.get_messages(session_id)
    return jsonify(messages)


@app.route("/api/sessions/<session_id>/chat", methods=["POST"])
def chat(session_id):
    """Send a message and get LLM response"""
    conv_mgr = app.config["CONV_MGR"]
    api_client = app.config["API_CLIENT"]
    hf = app.config["HEARTFLOW"]
    cfg = app.config["XINCHONG_CFG"]

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Step 1: Add user message
    conv_mgr.add_message(session_id, "user", user_message)

    # Step 2: HeartFlow cognitive analysis
    cognitive = conv_mgr.process_with_heartflow(user_message, session_id)

    # Step 3: Check for crisis
    if cognitive.get("crisis_flag"):
        crisis_reply = "💙 我注意到你提到了关于结束生命或伤害自己的想法。\n\n我想让你知道，你的感受是真实的，而且有人关心你。\n\n请记住：\n• 你并不孤单\n• 困难只是暂时的\n• 寻求帮助是勇敢的表现\n\n📞 心理援助热线（中国）：400-161-9995\n📞 北京心理危机研究与干预中心：010-82951332\n\n如果你在危险中，请立即联系当地的紧急服务。"

        conv_mgr.add_message(session_id, "assistant", crisis_reply, {"type": "crisis_intervention"})
        return jsonify({
            "role": "assistant",
            "content": crisis_reply,
            "cognitive": cognitive,
            "type": "crisis_intervention",
        })

    # Step 4: Build LLM messages
    messages = conv_mgr.get_conversation_for_llm(session_id)

    # Inject cognitive context
    cognitive_ctx = hf.generate_system_context(session_id)
    # Prepend cognitive context as a system message (before last user)
    # Find last user message and add cognitive context
    for i, msg in enumerate(messages):
        if msg["role"] == "system":
            msg["content"] += "\n" + cognitive_ctx

    # Step 5: Call LLM
    if not api_client:
        reply = f"⚠️ API 未配置。请在 config.yaml 中设置 API key。\n\n你发送的消息: {user_message}\n\nHeartFlow 分析:\n- 情绪: {cognitive.get('emotion', {}).get('primary_emotion', 'neutral')}\n- TGB和谐度: {cognitive.get('tgb', {}).get('overall', 0.5):.2f}\n- 意识状态: {cognitive.get('consciousness', {}).get('consciousness_state', 'unknown')}"
        conv_mgr.add_message(session_id, "assistant", reply, {"type": "no_api"})
        return jsonify({
            "role": "assistant",
            "content": reply,
            "cognitive": cognitive,
        })

    try:
        # Use streaming
        provider = data.get("provider")
        if provider and not api_client.is_provider_available(provider):
            return jsonify({"error": f"Provider '{provider}' not available"}), 400

        full_response = ""
        model_used = ""

        def generate():
            nonlocal full_response, model_used
            for chunk in api_client.chat_stream(messages, provider=provider):
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk}, ensure_ascii=False)}\n\n"
            model_used = api_client.chat(messages, provider=provider)[1] if not model_used else model_used

        resp = Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
        )
        resp.headers["Cache-Control"] = "no-cache"
        resp.headers["X-Accel-Buffering"] = "no"

        # Save full response after streaming
        conv_mgr.add_message(session_id, "assistant", full_response, {
            "model": model_used,
            "cognitive": cognitive,
        })

        return resp

    except Exception as e:
        import traceback
        traceback.print_exc()
        error_reply = f"⚠️ API 调用失败: {str(e)}"
        conv_mgr.add_message(session_id, "assistant", error_reply, {"type": "error"})
        return jsonify({
            "role": "assistant",
            "content": error_reply,
            "cognitive": cognitive,
            "error": str(e),
        })


@app.route("/api/chat", methods=["POST"])
def chat_simple():
    """Non-streaming chat (for API use)"""
    conv_mgr = app.config["CONV_MGR"]
    api_client = app.config["API_CLIENT"]
    hf = app.config["HEARTFLOW"]

    data = request.get_json()
    session_id = data.get("session_id")
    user_message = data.get("message", "").strip()
    provider = data.get("provider")

    if not session_id:
        session = conv_mgr.create_session()
        session_id = session.id

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    conv_mgr.add_message(session_id, "user", user_message)
    cognitive = conv_mgr.process_with_heartflow(user_message, session_id)

    if cognitive.get("crisis_flag"):
        crisis_reply = "💙 我注意到你的表达。如果你有伤害自己的想法，请拨打心理援助热线 400-161-9995"
        conv_mgr.add_message(session_id, "assistant", crisis_reply)
        return jsonify({"response": crisis_reply, "cognitive": cognitive, "session_id": session_id})

    messages = conv_mgr.get_conversation_for_llm(session_id)
    for msg in messages:
        if msg["role"] == "system":
            msg["content"] += hf.generate_system_context(session_id)

    if not api_client:
        return jsonify({"error": "API not configured", "cognitive": cognitive}), 500

    try:
        reply, model = api_client.chat(messages, provider=provider)
        conv_mgr.add_message(session_id, "assistant", reply, {"model": model})
        return jsonify({
            "response": reply,
            "cognitive": cognitive,
            "session_id": session_id,
            "model": model,
        })
    except Exception as e:
        return jsonify({"error": str(e), "cognitive": cognitive}), 500


@app.route("/api/heartflow/analyze", methods=["POST"])
def analyze():
    """Analyze text with HeartFlow cognitive engine"""
    hf = app.config["HEARTFLOW"]
    data = request.get_json()
    text = data.get("text", "")
    session_id = data.get("session_id", "default")

    result = hf.process(text, session_id=session_id)
    return jsonify({
        "tgb": result.tgb,
        "emotion": result.emotion,
        "consciousness": result.consciousness,
        "self_evolution": result.self_evolution,
        "reasoning_chain": result.reasoning_chain,
        "alternatives": result.alternatives,
        "confidence": result.confidence,
        "crisis_flag": result.crisis_flag,
    })


@app.route("/api/status", methods=["GET"])
def status():
    """Get system status"""
    api_client = app.config.get("API_CLIENT")
    providers = api_client.list_providers() if api_client else []
    return jsonify({
        "app": "心虫 (Xinchong)",
        "version": "1.0.0",
        "providers": providers,
        "default_provider": api_client.get_default_provider() if api_client else None,
        "api_ready": app.config.get("API_READY", False),
        "heartflow": True,
    })


if __name__ == "__main__":
    cfg = app.config["XINCHONG_CFG"]
    host = cfg.get("app", {}).get("host", "0.0.0.0")
    port = cfg.get("app", {}).get("port", 8765)
    debug = cfg.get("app", {}).get("debug", False)
    print(f"🐛 心虫 (Xinchong) starting on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug, threaded=True)
