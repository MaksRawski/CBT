TARGET = num2lcd.asm
IP = 192.168.0.157

BIN = $(basename $(TARGET)).bin

$(BIN): $(TARGET)
	customasm -f binary ../cbt.cpu $(TARGET) -o $(BIN)

upload: $(BIN)
	curl -X POST -F "bin=@$(realpath $(BIN))" http://$(IP)/upload_bin

run:
	curl http://$(IP)/rst

clean:
	rm $(BIN)
