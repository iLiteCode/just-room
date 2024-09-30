import sys
import pickle

if len(sys.argv) < 2:
    print('Error: No message provided')
    sys.exit(1)

print(f"Received message: {sys.argv[1]}")

try:
    with open('spam_classifier_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully")  

    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    print("Vectorizer loaded successfully")  
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)


message = sys.argv[1]


try:
    message_vector = vectorizer.transform([message])
    print(f"Message vectorized: {message_vector.shape}") 
except Exception as e:
    print(f"Error during vectorization: {e}")
    sys.exit(1)


try:
    prediction = model.predict(message_vector)[0]
    print("prediction=====>",prediction)
    print('spam' if prediction == 1 else 'ham') 
except Exception as e:
    print(f"Error during prediction: {e}")
    sys.exit(1)
