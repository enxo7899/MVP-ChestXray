"""
Flask Web Application for Chest X-Ray Classifier
Ministria e Shëndetësisë - Republika e Shqipërisë
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import io
from engine_chest import predict_chest
from translations import translate_pathology

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/')
def index():
    """Render the main interface."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handles image upload, runs prediction, and returns results.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        try:
            # Read image data
            image_data = file.read()
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            image_array = np.array(image)
            
            # Run prediction
            results = predict_chest(image_array)
            
            # Sort by probability
            sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
            
            # Format response with translations
            response = {
                'success': True,
                'image_shape': image_array.shape,
                'predictions': [
                    {
                        'pathology': translate_pathology(pathology),
                        'pathology_english': pathology,
                        'probability': float(prob),
                        'percentage': float(prob * 100)
                    }
                    for pathology, prob in sorted_results
                ],
                'top_3': [
                    {
                        'pathology': translate_pathology(pathology),
                        'pathology_english': pathology,
                        'probability': float(prob),
                        'percentage': float(prob * 100)
                    }
                    for pathology, prob in sorted_results[:3]
                ]
            }
            
            return jsonify(response)
        
        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 400
    
    return jsonify({'error': 'Unknown error'}), 500


if __name__ == '__main__':
    # For production deployment
    app.run(host='0.0.0.0', port=7860, debug=False)
