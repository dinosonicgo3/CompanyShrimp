from flask import Blueprint, render_template, request, jsonify
import logging

main_bp = Blueprint('main', __name__)
logger = logging.getLogger("shrimp.app")

# 模擬任務隊列
task_queue = []

@main_bp.route('/')
def index():
    return render_template('index.html', tasks=task_queue)

@main_bp.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Missing URL"}), 400
    
    task = {
        "id": len(task_queue) + 1,
        "url": url,
        "status": "pending"
    }
    task_queue.append(task)
    logger.info(f"已新增任務: {url}")
    return jsonify({"status": "success", "task": task})

@main_bp.route('/api/status')
def get_status():
    return jsonify({
        "status": "running",
        "queue_count": len(task_queue),
        "recent_tasks": task_queue[-5:]
    })
