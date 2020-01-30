# Encryptoк
Шифровани и взлом шифров Цезаря Виженера и Вернама  

#Запуск#
* Шифрование ```./encryptor.py encode --cipher {caesar,vigenere} --key {number|word} [--input-file input.txt] [--output-file output.txt]```  
* Дешифровка ```./encryptor.py decode --cipher [caesar,vigenere] --key {number for caesar or word for vigenere} [--input-file input.txt] [--output-file output.txt]```
* Взлом ```./encryptor.py hack [--input-file input.txt] [--output-file output.txt] --model-file {model}```
