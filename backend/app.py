from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///disaster_relief.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Models
class Center(db.Model):
    __tablename__ = 'centers'
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.String(50), unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    water_stock = db.Column(db.Integer, default=0)
    food_stock = db.Column(db.Integer, default=0)
    tent_stock = db.Column(db.Integer, default=0)

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(50), unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    need_type = db.Column(db.String(50), nullable=False)
    urgency = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    allocated_center_id = db.Column(db.String(50), nullable=True)
    resources_sent = db.Column(db.Integer, nullable=True)
    distance = db.Column(db.Float, nullable=True)

class Allocation(db.Model):
    __tablename__ = 'allocations'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(50), nullable=False)
    center_id = db.Column(db.String(50), nullable=False)
    resources_sent = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/reports', methods=['POST'])
def create_report():
    """Save a new disaster request"""
    try:
        data = request.json
        
        # Generate request ID
        request_count = Request.query.count()
        request_id = f"REQ{request_count + 1:04d}"
        
        new_request = Request(
            request_id=request_id,
            lat=float(data['lat']),
            lon=float(data['lon']),
            people=int(data['people']),
            need_type=data['need_type'],
            urgency=data['urgency']
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        # Emit WebSocket event
        socketio.emit('new_report', {
            'request_id': request_id,
            'lat': new_request.lat,
            'lon': new_request.lon,
            'people': new_request.people,
            'need_type': new_request.need_type,
            'urgency': new_request.urgency
        })
        
        return jsonify({
            'success': True,
            'request_id': request_id,
            'message': 'Report created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/reports', methods=['GET'])
def get_reports():
    """Return all reports"""
    try:
        requests_list = Request.query.all()
        
        return jsonify({
            'success': True,
            'reports': [{
                'request_id': r.request_id,
                'lat': r.lat,
                'lon': r.lon,
                'people': r.people,
                'need_type': r.need_type,
                'urgency': r.urgency,
                'status': r.status,
                'allocated_center_id': r.allocated_center_id,
                'resources_sent': r.resources_sent,
                'distance': r.distance,
                'created_at': r.created_at.isoformat() if r.created_at else None
            } for r in requests_list]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/centers', methods=['GET'])
def get_centers():
    """Return all centers"""
    try:
        centers = Center.query.all()
        
        return jsonify({
            'success': True,
            'centers': [{
                'center_id': c.center_id,
                'lat': c.lat,
                'lon': c.lon,
                'water_stock': c.water_stock,
                'food_stock': c.food_stock,
                'tent_stock': c.tent_stock
            } for c in centers]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/centers', methods=['POST'])
def create_center():
    """Create a new center (admin only)"""
    try:
        data = request.json
        
        new_center = Center(
            center_id=data['center_id'],
            lat=float(data['lat']),
            lon=float(data['lon']),
            water_stock=int(data.get('water_stock', 0)),
            food_stock=int(data.get('food_stock', 0)),
            tent_stock=int(data.get('tent_stock', 0))
        )
        
        db.session.add(new_center)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Center created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/optimize', methods=['POST'])
def optimize_allocation():
    """Run allocation algorithm"""
    try:
        from services.allocator import allocate_resources
        
        # Get all pending requests and available centers
        pending_requests = Request.query.filter_by(status='pending').all()
        centers = Center.query.all()
        
        # Convert to dictionaries
        requests_data = [{
            'request_id': r.request_id,
            'lat': r.lat,
            'lon': r.lon,
            'people': r.people,
            'need_type': r.need_type,
            'urgency': r.urgency
        } for r in pending_requests]
        
        centers_data = [{
            'center_id': c.center_id,
            'lat': c.lat,
            'lon': c.lon,
            'water_stock': c.water_stock,
            'food_stock': c.food_stock,
            'tent_stock': c.tent_stock
        } for c in centers]
        
        # Run allocation
        allocations, updated_centers = allocate_resources(centers_data, requests_data)
        
        # Save allocations to database
        for alloc in allocations:
            new_allocation = Allocation(
                request_id=alloc['request_id'],
                center_id=alloc['center_id'],
                resources_sent=alloc['resources_sent'],
                distance=alloc['distance']
            )
            db.session.add(new_allocation)
            
            # Update request status
            req = Request.query.filter_by(request_id=alloc['request_id']).first()
            if req:
                req.status = 'allocated'
                req.allocated_center_id = alloc['center_id']
                req.resources_sent = alloc['resources_sent']
                req.distance = alloc['distance']
        
        # Update center stocks
        for center_data in updated_centers:
            center = Center.query.filter_by(center_id=center_data['center_id']).first()
            if center:
                center.water_stock = center_data['water_stock']
                center.food_stock = center_data['food_stock']
                center.tent_stock = center_data['tent_stock']
        
        db.session.commit()
        
        # Emit WebSocket event
        socketio.emit('allocations_updated', {
            'allocations': allocations,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return jsonify({
            'success': True,
            'allocations': allocations,
            'message': f'Allocated {len(allocations)} requests'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/allocations', methods=['GET'])
def get_allocations():
    """Get all allocations"""
    try:
        allocations = Allocation.query.all()
        
        return jsonify({
            'success': True,
            'allocations': [{
                'request_id': a.request_id,
                'center_id': a.center_id,
                'resources_sent': a.resources_sent,
                'distance': a.distance,
                'created_at': a.created_at.isoformat() if a.created_at else None
            } for a in allocations]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/predict', methods=['GET'])
def predict_demand():
    """Predict resource demand for next 7 days"""
    try:
        from services.prediction import predict_resource_demand
        
        predictions = predict_resource_demand()
        
        return jsonify({
            'success': True,
            'predictions': predictions
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# WebSocket events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
