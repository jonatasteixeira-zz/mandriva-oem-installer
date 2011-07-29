NAME=oem-installer


all: 
	chmod +x script/oem-installer
	chmod +x script/qt4
	chmod +x script/translate


install:
	chmod +x tmp/${NAME}
	head -n1 tmp/${NAME} > tmp/new
	mv tmp/new tmp/${NAME}
	echo "/usr/share/${NAME}/script/${NAME} \$$1" >> tmp/${NAME}


clean:
	head -n1 tmp/${NAME} > tmp/new
	mv tmp/new tmp/${NAME}

run:
	script/oem-installer
qt4:
	script/qt4

