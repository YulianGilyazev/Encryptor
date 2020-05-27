# Encryptoк
Шифровани и взлом шифров Цезаря Виженера и Вернама  

# Использование #
* Шифрование ```./encryptor.py encode --cipher {caesar,vigenere} --key {number|word} [--input-file input.txt] [--output-file output.txt]```  
* Дешифровка ```./encryptor.py decode --cipher [caesar,vigenere] --key {number for caesar or word for vigenere} [--input-file input.txt] [--output-file output.txt]```
* Взлом ```./encryptor.py hack [--input-file input.txt] [--output-file output.txt] --model-file {model}```
* Обучение ```./encryptor.py train --text-file {input.txt} --model-file {model}```
