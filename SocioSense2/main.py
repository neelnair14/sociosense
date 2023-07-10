import dotenv
from dotenv import load_dotenv



import streamlit as st

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

load_dotenv()

def predict_text_sentiment_analysis_sample(
    project: str,
    endpoint_id: str,
    content: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
    ):

    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    instance = predict.instance.TextSentimentPredictionInstance(
        content=content,
    ).to_value()
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/text_sentiment_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    for prediction in predictions:
        print(" prediction:", dict(prediction))

    return predictions

# [END aiplatform_predict_text_sentiment_analysis_sample]


def generate_prompt( input_text, **kwargs):
    return f"{input_text}"

def submit():
    prompt = generate_prompt(**st.session_state)
    output = predict_text_sentiment_analysis_sample(
    project="873086289597",
    endpoint_id="5868397022649778176",
    location="us-central1",
    content= prompt
    )
    for out in output:

        st.session_state["output"] = dict(out) 


#UI Initialisation
if "output" not in st.session_state:
    st.session_state["output"] = "--"

st.title("SocioSense")
st.header("Section 1")
st.markdown("[Section 1](#section-1)")
st.subheader("Let us be your PR Team!")
st.subheader("The higher your text is rated, the more negative it is. The lower it is rated, the more positive :)")

with st.form(key="trip_form"):
    
    
    st.text_area("Input your text here", height=200,key="input_text")
    st.form_submit_button("Submit", on_click=submit)

st.subheader("Prediction Result: ")
st.write(st.session_state.output)
