====
Burp Extension to auto manipulate AES En/Decryption
====
#简介
这个插件只写了AES256/CBC/PKCS7Padding 加密方式，其他例如EBC PKCS5Padding nopadding 等不同加密类型，修改AEScrypt_Script.py的加密代码。<br><br>
插件可以自动加解密AES数据，在数据界面添加AESkiller选项卡，对AESkiller界面内的数据修改可以直接自动修改成加密数据。<br><br>
开始是想着把所有功能都写在扩展内，不过jython对加密模块支持不行，所以抽取出独立脚本，大家修改也方便。<br><br>
#配置
AESKEY: 加密key<br>
AES IV: 初始化向量必须是HEX编码的 <br>
AES Mode: 当时是给多种加密方式占的输入坑，现在没用到<br>
Parameters: 这是加解密的提取参数名，只对指定的参数(支持多个参数)进行解密，格式：data|cryptdata|ret<br>
Pyhton path:Python 路径<br>
Script  path: 加解密脚本路径<br>
 ![image](https://github.com/arschlochnop/aeskiller/blob/master/screenshots/video.gif)