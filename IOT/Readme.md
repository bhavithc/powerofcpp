```
git clone https://github.com/openssl/openssl.git
cd openssl
./Configure
make
# make test
make install 
cd ..
```

```
git clone https://github.com/eclipse/paho.mqtt.c.git
cd paho.mqtt.c
make
sudo make install
cd ..
```

```
pip install --upgrade certifi
python3 -m venv myenv
source myenv/bin/activate
pip3 install paho-mqtt
```

```
gcc main.c -l paho-mqtt3cs
```