# Solitaire Algorithm
Solitaire Crypto Algorithm implemented by aaron

This implementation uses secret passphrase as key to shuffle the deck, and you know what they say _"the longer the better"_.
> Remember, though, that there are only about 1.4 bits of randomness per character in standard English. You’re going to want at least an 64-character passphrase to make this secure; I recommend at least 80 characters, just in case. Sorry; you just can’t get good security with a shorter key. - Bruce Schneier.   
 
This passphrase is stored in `passphrase.txt`, this is the "key", so for example if you want to encrypt a message on computer A and decrypt it on remote computer B, you should share the `passhprase.txt`, and use the same sized deck located in `deck.txt`.   
### Reqs:
- `Path`
- `argparse`

### Instructions
## 
**Encrypt**:    
`python3 solitaire.py -e "HODL DOGE COIN. 2021"`   
    
![Encrypt](https://i.imgur.com/WzRb3L3.png)   
## 
**Decrypt**:   
     
`python3 solitaire.py -d "RFNFNQIDSSOPBHP"`   
     
![Decrypt](https://i.imgur.com/N3bo55P.png)      
## 
**Encrypt Verbose**:    
      
`python3 solitaire.py -e -v "HODL DOGE COIN. 2021"`    
     
![Encrypt w. Verbosity](https://i.imgur.com/lb36xDX.png)       
## 
**Decrypt Verbose**:      
      
`python3 solitaire.py -d -v "RFNFNQIDSSOPBHP"`    
     
![Decrypt w. Verbosity](https://i.imgur.com/DD0eugG.png)      
## 
**Both Encrypt and Decrypt**:      
     
`python3 solitaire.py -e "HOLD DOGE COIN. 2021" | xargs python3 solitaire.py -d`       
     
![Encrypt and Decrypt](https://i.imgur.com/k43mPtG.png)         
 
 
### References
[Solitaire Encryption Algorithm](https://www.schneier.com/academic/solitaire/)   
[Solitaire Algorithm Simplified](http://nifty.stanford.edu/2006/mccann-sssolitaire/SSSolitaire.pdf)
