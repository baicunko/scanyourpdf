#Make your PDF look scanned.
#Idea from the post in HN. Make a Gist with the command code.
#https://gist.github.com/jduckles/29a7c5b0b8f91530af5ca3c22b897e10
INPUT_FILE=$1
convert -density 150 ${INPUT_FILE} -colorspace gray -linear-stretch 3.5%x10% -blur 0x0.5 -attenuate 0.25 +noise Gaussian  -rotate 1.0  aux_output.pdf
gs -dSAFER -dBATCH -dNOPAUSE -dNOCACHE -sDEVICE=pdfwrite -sColorConversionStrategy=LeaveColorUnchanged -dAutoFilterColorImages=true -dAutoFilterGrayImages=true -dDownsampleMonoImages=true -dDownsampleGrayImages=true -dDownsampleColorImages=true -sOutputFile=document_flat.pdf aux_output.pdf
rm aux_output.pdf