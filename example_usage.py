#!/usr/bin/env python3
"""
Example usage of the Language Identification API.
Run this after starting the API server.
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_api():
    """Test the Language Identification API with various examples."""
    
    print("🚀 Testing Language Identification API")
    print("=" * 50)
    
    # Test texts in different languages
    test_texts = [
        ("Hello, how are you today?", "English"),
        ("Bonjour, comment allez-vous?", "French"),
        ("Hola, ¿cómo estás?", "Spanish"),
        ("Guten Tag, wie geht es Ihnen?", "German"),
        ("Ciao, come stai?", "Italian"),
        ("Olá, como você está?", "Portuguese"),
        ("Привет, как дела?", "Russian"),
        ("こんにちは、元気ですか？", "Japanese"),
        ("안녕하세요, 어떻게 지내세요?", "Korean"),
        ("你好，你好吗？", "Chinese"),
    ]
    
    # Wait for the API to be ready
    print("⏳ Waiting for API to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get("model_loaded"):
                    print("✅ API is ready!")
                    break
                else:
                    print("⏳ Model is loading...")
        except requests.exceptions.RequestException:
            print(f"⏳ Waiting for API... ({i+1}/30)")
        time.sleep(2)
    else:
        print("❌ API is not responding. Make sure the server is running.")
        return
    
    print()
    
    # Test each text
    for text, expected_lang in test_texts:
        try:
            print(f"📝 Testing: '{text}' (Expected: {expected_lang})")
            
            response = requests.post(
                f"{API_BASE_URL}/predict",
                json={"text": text},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                top_prediction = data["predictions"][0]
                confidence = top_prediction["confidence"]
                detected_lang = top_prediction["language"]
                
                print(f"   🎯 Detected: {detected_lang} (confidence: {confidence:.4f})")
                
                if confidence > 0.8:
                    print("   ✅ High confidence prediction")
                elif confidence > 0.5:
                    print("   ⚠️  Medium confidence prediction")
                else:
                    print("   ❓ Low confidence prediction")
                    
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        print()
    
    # Test supported languages endpoint
    print("🌍 Testing supported languages endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/supported-languages")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Total supported languages: {data['total_languages']}")
            print(f"   📋 First 10 languages: {data['languages'][:10]}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
    
    print()
    print("🎉 API testing completed!")
    print(f"🔗 Visit {API_BASE_URL}/docs for interactive documentation")

if __name__ == "__main__":
    test_api()