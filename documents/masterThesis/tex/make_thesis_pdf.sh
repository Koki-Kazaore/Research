#!/bin/sh

# PDFを結合
pdfunite top.pdf main.pdf thesis.pdf

# PDFを表示
evince thesis.pdf &

