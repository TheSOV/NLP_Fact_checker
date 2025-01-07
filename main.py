from flask import Flask, send_from_directory, request, jsonify
from flask_restful import Api, Resource
import os
import traceback
from dotenv import load_dotenv
from flows.fact_checker_flow import FactCheckerFlow
from flows.get_summarized_source_flow import GetSummarizedSourceFlow
from flows.internet_fact_checker_flow import InternetFactCheckerFlow
from crews.generic_translation_crew import generic_translation_crew
from tools.search_manager import SearchManager
from utils.embeddings import embeddings
import webbrowser
import threading

# Load environment variables
load_dotenv()

# Initialize embeddings at startup
embeddings

app = Flask(__name__)
api = Api(app)

# Get the absolute path to the web directory
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')

# Initialize search manager at startup
search_manager = SearchManager()

class FactCheckerAPI(Resource):
    def post(self):
        """API endpoint for fact checking"""
        try:
            data = request.get_json()
            if not data or 'statement' not in data:
                return {'error': 'Missing statement in request'}, 400

            statement = data['statement']
            print(f"Received statement: {statement}")  # Debug print
            flow = FactCheckerFlow(user_input=statement)
            result = flow.kickoff()
            
            # Convert FactCheckerState to dictionary
            result_dict = result.translation if hasattr(result, 'translation') else {}
            result_dict['confidence_score'] = result.confidence_score if hasattr(result, 'confidence_score') else None
            
            print(f"Flow result: {result_dict}")  # Debug print
            return jsonify(result_dict)

        except Exception as e:
            print(f"Error in FactCheckerAPI: {e}")  # Debug print
            print(traceback.format_exc())  # Print full traceback
            return {'error': str(e), 'traceback': traceback.format_exc()}, 500

class InternetFactCheckerAPI(Resource):
    def post(self):
        """API endpoint for internet fact checking"""
        try:
            data = request.get_json()
            if not data or 'statement' not in data:
                return {'error': 'Missing statement in request'}, 400

            statement = data['statement']
            print(f"Received statement for internet fact check: {statement}")  # Debug print
            flow = InternetFactCheckerFlow(user_input=statement)
            result = flow.kickoff()
            
            # Convert InternetFactCheckerState to dictionary
            result_dict = result.translation if hasattr(result, 'translation') else {}
            result_dict['confidence_score'] = result.confidence_score if hasattr(result, 'confidence_score') else None
            
            print(f"Internet flow result: {result_dict}")  # Debug print
            return jsonify(result_dict)

        except Exception as e:
            print(f"Error in InternetFactCheckerAPI: {e}")  # Debug print
            print(traceback.format_exc())  # Print full traceback
            return {'error': str(e), 'traceback': traceback.format_exc()}, 500

class SummarizedSourceAPI(Resource):
    def post(self):
        """API endpoint for getting summarized source"""
        try:
            data = request.get_json()
            if not data or 'source' not in data:
                return {'error': 'Missing source in request'}, 400

            source = data['source']
            target_language = data.get('target_language', 'English')
            
            flow = GetSummarizedSourceFlow(
                source=source,
                target_language=target_language
            )
            result = flow.kickoff()
            print(f"Flow result: {result}")  # Debug print
            
            # Convert state to dictionary for JSON serialization
            response = {
                'source': source,
                'target_language': target_language,
                'summary': result.translated_summary
            }
            return jsonify(response)

        except Exception as e:
            print(f"Error in SummarizedSourceAPI: {e}")  # Debug print
            print(traceback.format_exc())  # Print full traceback
            return {'error': str(e), 'traceback': traceback.format_exc()}, 500

# Register API endpoints
api.add_resource(FactCheckerAPI, '/api/fact-check')
api.add_resource(InternetFactCheckerAPI, '/api/fact-check-internet')
api.add_resource(SummarizedSourceAPI, '/api/summarize-source')

@app.route('/')
def index():
    """Serve the main index.html file"""
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/<path:path>')
def serve_web_files(path):
    """Serve all other files from the web directory"""
    return send_from_directory(WEB_DIR, path)

@app.route('/api/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data or 'target_language' not in data:
            return {'error': 'Missing text or target language'}, 400

        text = data['text']
        target_language = data['target_language']

        # Use the generic translation crew
        result = generic_translation_crew.kickoff(inputs={
            'content': text,
            'target_language': target_language
        })

        return jsonify({
            'translated_text': result.raw,
            'source_text': text,
            'target_language': target_language
        })

    except Exception as e:
        print(f"Error in translation: {e}")
        print(traceback.format_exc())
        return {'error': str(e), 'traceback': traceback.format_exc()}, 500

if __name__ == '__main__':
    # Ensure the web directory exists
    if not os.path.exists(WEB_DIR):
        raise FileNotFoundError(f"Web directory not found at: {WEB_DIR}")
    
    
    def open_browser():
        webbrowser.open('http://localhost:5555')
    
    threading.Timer(2, open_browser).start()
    
    print(f"Serving web files from: {WEB_DIR}")
    app.run(debug=False, port=5555)
