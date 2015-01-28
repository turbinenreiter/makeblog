all:
	python3.3 makeblog.py
	cp -a ./res/. ../blog/
	cp ./content/*.gif ../blog/
	cp ./content/*.jpg ../blog/

clean:
	rm -rf ../blog/*
