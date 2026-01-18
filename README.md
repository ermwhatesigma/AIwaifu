# AIwaifu
This is an project that uses ollama so you can chat with an ai. While a waifu png will be displayed on the screen. The chat place is on a different chat box in a tk windows so you can chat with th local ai model.  
In my demo gif i have used my own refined AI model that you can find on: https://ollama.com/ermwhatesigma420/Hanna  
I used the ermwhatesigma420\hanna:7B in this demo gif here below. Remember this project is still experimental  
**sorry for the low gif quality**  
![Demo](waifu/waifu.gif)  
# Install ollama
The model in the waifu.py in the repository is ermwhatesigma420\hanna the smaller 2.7B model might not work as great as the 7B model but it still works fine  
Instalation. Make sure you have ollama installed --> https://ollama.com/download  
Install my models or choose your own  
```bash
ollama pull ermwhatesigma420\hanna #if you wanna use the 7B model run
#ollama pull ermwhatesigma420\hanna:7B
#if you wanna test the installed models run : ollama run ermwhatesigma430\hanna
```
If you choose to pull the 7b model make sure to edit in the main code waifu.py into that ollama model  
Before runing the waifu.py make sure you have all the pip installed
```bash
pip install pygame pywin32 ollama
```
Also after you have everything installed python libraries and the rest don't forget to serve ollama so run.
```bash
ollama serve
```
In the background so ollama will work in the python script.
# Run the waifu.py
Make sure you have all the pips installed. If you have then you can skip the pip install -r requirements.txt  
**Windows**
```bash
git clone https://github.com/ermwhatesigma/AIwaifu
cd AIwaifu
pip install -r requirements.txt #only if you didn't install the pyton librearies already
python waifu.py #python3 waifu.py wich one you use
#make sure ollama is already runing in the backgorund with --> ollama serve
```
**Linux**  
Didn't test yet will try to review it soon.  
 

**note**: I will try to add a button in the tk window that lats the AI waifu also speak real words instead of only reading what she says. And i will also try to make a speech-to-text-ai-text-speech.  
So you tlk in the mic gets converted to text ai reads the text spits out text and filters it to speech. Also with the speech to speech i will add a gaming overlay so instead of the waifu grabing the whole chunk of the screen it would only grab a small right corner.
