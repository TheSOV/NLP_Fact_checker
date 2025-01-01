from flask import Flask, send_from_directory, request, jsonify
from flask_restful import Api, Resource
import os
import traceback
from dotenv import load_dotenv
from flows.fact_checker_flow import FactCheckerFlow
from flows.get_summarized_source_flow import GetSummarizedSourceFlow
from crews.generic_translation_crew import generic_translation_crew
from tools.search_manager import SearchManager

# Load environment variables
load_dotenv()

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
            
            print(f"Flow result: {result_dict}")  # Debug print
            return jsonify(result_dict)

        except Exception as e:
            print(f"Error in FactCheckerAPI: {e}")  # Debug print
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

@app.after_request
def add_header(response):
    """Add headers to prevent caching during development"""
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    # Ensure the web directory exists
    if not os.path.exists(WEB_DIR):
        raise FileNotFoundError(f"Web directory not found at: {WEB_DIR}")
    
    print(f"Serving web files from: {WEB_DIR}")
    app.run(debug=True, port=5000)
