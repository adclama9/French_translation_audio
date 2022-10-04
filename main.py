import gradio as gr
from transformers import pipeline
from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import torch
from fairseq.utils import move_to_cuda
import pywhisper
import gc
gc.collect()
torch.cuda.empty_cache()

asr_model = pywhisper.load_model("medium") # large requires too much vram! 10 gigs


translation_pipeline = pipeline('translation_en_to_fr',model = "Helsinki-NLP/opus-mt-en-fr" ) #This model version is built for en- to -fr , less mistakes

models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
    "facebook/tts_transformer-fr-cv7_css10",
    arg_overrides={"vocoder": "hifigan", "fp16": False}
)

model = models[0]
model = model.to(torch.device("cuda:0")) if torch.cuda.is_available() else model

TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
generator = task.build_generator(models, cfg)


def transcribe_translate(audio):
    text_en = asr_model.transcribe(audio, language = 'en')['text']
    
    text_fr = translation_pipeline(text_en) # for some reason all audio converted to all caps and it translates differently???
    text_fr = text_fr[0]['translation_text']       # good evening = bonsoir  but GOOD EVENING = BONNES SÉANCES . WEIRD

    sample = TTSHubInterface.get_model_input(task, text_fr)
    sample = move_to_cuda(sample) if torch.cuda.is_available() else sample

    wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)
    wav = wav.to('cpu')
    wav = wav.numpy()
    print(wav.dtype)

    return text_en,text_fr , (rate,wav)


iface = gr.Interface(
    fn=transcribe_translate, 
    inputs=[
        gr.Audio(source="microphone", type="filepath")
    ],
    outputs=[
        gr.Textbox(label= "English Transcription"),
        gr.Textbox(label= "French Translation"),
        gr.Audio(label = "French Audio")
    ],
    live=True)

iface.launch(share=True)

