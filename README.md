# ResearchCode
research related analysis code, Weaver lab

FRET_Raichu: to process images to calculate FRET index; need a YFP, CFP, and FRET image to calculate ratios.

nuclear_loc: basic setup to process large image stitches from 6D images; takes DAPI and some second stain and determines
nuclear localization of the second stain. Uses image segmentation to output nice outline and count images of the nuclei.
Has setup for zprojection of zstack, using Watershed Segmentation algorithm to find nuclei and cells, and calculating
overlap between two channels.
