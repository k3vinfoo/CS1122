import binascii

#Open the file being recovered as readable binary file, read the data, then close file
file = open("cyber_security_file_recovery", "rb")
byte = file.read()
file.close()

#Convert bytes to hex
hexadecimal = binascii.hexlify(byte)
hexadecimal = hexadecimal.decode("utf-8")

def recoverPNGs():
	#Files which will contain hexdump of recovered PNGs
	png1 = open("png1", 'wb')
	png2 = open("png2", 'wb')
	png3 = open("png3", 'wb')
	png4 = open("png4", 'wb')
	png5 = open("png5", 'wb')
	png6 = open("png6", 'wb')
	pngs = [png1, png2, png3, png4, png5, png6]

	#File signatures for PNGs
	pngHead = '89504e470d0a1a0a'
	pngTrail = '49454e44ae426082'

	head_start = 0
	trailer_start = 0

	#Lists will contain head and trailer signatures of all PNGs
	pngHeadLst= []
	pngTrailLst = []

	while(hexadecimal.find(pngHead,head_start) != -1):
		header_index = hexadecimal.find (pngHead, head_start)
		trailer_index = hexadecimal.find (pngTrail, trailer_start)

		pngHeadLst.append(header_index)
		pngTrailLst.append(trailer_index+len(pngTrail))

		head_start = header_index + len(pngHead) + 1
		trailer_start = trailer_index + len(pngTrail) + 1

	for i in range(len(pngHeadLst)):
		binary = binascii.unhexlify(hexadecimal[pngHeadLst[i] : pngTrailLst[i]])
		pngs[i].write(binary)

def recoverPDFs():
	#Files which will contain hexdump of recovered PDFs
	pdf1 = open("pdf1", 'wb')
	pdf2 = open("pdf2", 'wb')
	pdf3 = open("pdf3", 'wb')
	pdf4 = open("pdf4", 'wb')
	pdfs = [pdf1, pdf2, pdf3, pdf4]

	#File signatures for PDFs
	pdfHead = '25504446'
	pdfTrail = '2525454f46'

	head_start = 0
	trailer_start = 0

	pdfHeadLst = []
	pdfTrailLst = []

	while(hexadecimal.find(pdfTrail, trailer_start) != -1):
		header_index = hexadecimal.find(pdfHead, head_start)
		trailer_index = hexadecimal.find(pdfTrail, trailer_start)

		if((header_index != -1) and (header_index not in pdfHeadLst)):
			pdfHeadLst.append(header_index)
		pdfTrailLst.append(trailer_index+len(pdfTrail))

		head_start = header_index + len(pdfHead) + 1
		trailer_start = trailer_index + len(pdfTrail) + 1

	#Write files containing all but the last PDF. (pdfHeadLst[i+1] would not work otherwise)
	for i in range(len(pdfHeadLst)-1):
		for j in range(len(pdfTrailLst)):
			if((pdfTrailLst[j] > pdfHeadLst[i]) and (pdfTrailLst[j] < pdfHeadLst[i+1])):
				binary = binascii.unhexlify(hexadecimal[pdfHeadLst[i] : pdfTrailLst[j]])
				pdfs[i].write(binary)
	#Writes final PDF file
	binary = binascii.unhexlify(hexadecimal[pdfHeadLst[len(pdfHeadLst)-1] : pdfTrailLst[len(pdfTrailLst)-1]])
	pdfs[len(pdfs)-1].write(binary)

recoverPDFs()
recoverPNGs()
