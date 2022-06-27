import regexcompare

#Example from https://en.wikipedia.org/wiki/Module:Excerpt/config (Revision 1092693703)
compareList = ['2021 United States Capitol attack', '2021 storming of the United States Capitol',
        '[Aa]bout', '[Tt]his', '[Tt]his article is about',
        '[Aa]griculture',
        '[Bb]roader',
        '[Cc]ampaignbox', '[Cc]ampaign',
        '[Cc]itations broken from PEIS limit',
        '[Cc]oor', '[Ll]ocation', '[Ll]ocation dec', '[Cc]o-ord',
        '[Cc]urrent', '[Ff]lux', '[Ll]ive', '[Oo]n ?going', '[Rr]ecent ?event', '[Rr]ecent news', '[Bb]reaking news',
        '[Dd]efault ?[Ss]ort', 'DEFAULT ?SORT',
        '[Dd]isplay ?title', 'DISPLAYTITLE', '[Ii]talic title',
        '[Ff]eatured ?article', '[Ff]eatured', '[Ff]eaturedSmall', 'FA topicon',
        '[Gg]ood [Aa]rticle','GA article', 'GA icon',
        '[G]lobal',
        '[Ii]nfo ?[Bb]ox', '[Rr]ow', '[Tt]axobox',
        '[Ll]ead ?missing', '[Ll]ede missing', '[Nn]o[ -]?[Ii]ntro', '[Nn]ointroduction', '[Nn]o[ -]?lead', '[Nn]o ?lede', '[Mm]issingintro', '[Ii]ntro[ -]?missing', '[Nn]o ?lead ?section',  '[Mm]issing lead', '[Mm]issing lede', '[Ll]ead absent', '[Ll]ede absent', '[Nn]o definition', '[Ii]ntroduction needed', '[Ii]ntroduction missing', '[Ii]ntro needed', '[Ll]ead required', '[Ll]ede required', '[Nn][Oo][Ll]',
        '[Ll]ead too long', '[Ll]ede ?too ?long', '[Ii]ntro ?length', '[Ll]ongintro', '[Ll]ong ?lead', '[Ll]ong ?lede', '[Ii]ntro[ -]?too[ -]?long', '[Ll][2T][Ll]', '[Ll]ead long',
        '[Ll]ead[ -]?rewrite', '[Ll]ead ?section', '[Vv]agueintro', '[Cc]leanup-lead', '[Ii]ntro', '[Oo]pening', '[Ll]ead', '[Ll]ede', '[Ii]ntro-?rewrite', '[Ll]ede rewrite', 'LEAD', 'LEDE', '[Rr]ewrite lead', '[Cc]leanup lead',
        '[Ll]ead[ -]?too[ -]?short', '[Ll]ede[ -]?too[ -]?short', '[Ee]xpand ?lead', '[Ee]xpand ?lede', '[Tt]oo ?[Ss]hort', '[Ss]hort ?intro', '[Ss]hort ?lead', '[Ii]ntro[ -]?too[ -]?short', '[Bb]uild lead', '[Ii]ntro-expand', 'XL', 'TSL', '[Ll]2[Ss]',
        '[Mm]ain[12]?', '[Mm]ain ?[Aa]rticles?', 'MAIN', '[Mm]ain page', '[Ss]ee ?main', '[Rr]eadmain', '[Ff]ull article', '[Hh]urricane main', '[Cc]omprehensive', '[Mm]ultiple ?issues',
        '[Nn]avbox', '[Nn]avigation', '[Nn]avigation ?[Bb]ox', '[Nn]avigation Template', '[Hh]ider hiding', '[Cc]?VG [Nn]avigation', '[Tt]ransNB', '[Nn]avtable',
        '[Oo]ther ?[Uu]ses?[13]?', '[Oo]thers?', '[Oo]ther ?[Mm]eanings?', '[Dd]istinguish', '[Aa]lternateuses', '[Oo]thervalues', '[Ff]or other uses',
        '^[Pp]p', '[Pp]p%-.+',
        '[Rr]edirect', '[Rr][Ee]dir', '[Rr]DR',
        '[Ss]ee ?[Aa]lso', '[Aa]lso', '[Ll]ooking', '[Rr]elated articles?', '[Ss]ee-[Aa]lso', '[Ll]ooking for', '[Ss]ee other', 'VT',
        '[Ss]emiprotected',
        '[Ss]hort[ -]?desc', 'SHORTDESC', '[Dd]escription', '[Bb]rief description',
        '[Ss]idebar', '[Hh]istory of ', '[Gg]enocide', '[Tt]imeline', '[Tt]opic', '[Aa]ntisemitism',
        '[Ss]poken',
        'TOC', '[Tt]oc ?[Ll]imit',
        '[Uu]se .+ English', '[Uu]se .+ spelling', '[Ee]ngvarB',
        '[Uu]se .+ dates',
        '[Ff]urther', '[Ff]urther2',
        '[Oo]utline',
        '[Ss]pecial[Cc]hars',
        '[Mm]erge from','[Mm]erge to',
        '[Vv]ery ?long', '[Ll]ong', '[Tt]oo ?big', '[Ll]ongish', '[Ss]horten', '[Ss]plit', '[Tt]oo[ -]?[Ll]ong', '2[Ll]', '2long', 'TOOLONG', '[Bb]igPage',
        '^[Ff][Oo][Rr][12]?', '[Ff]or ?the',

        '[Aa]dditional ?[Cc]itations?', '[Aa]dd? ?ref', '[Cc]itations ?[Mm]issing', '[Cc]itations ?[Nn]eeded', '[Cc]ite ?[Ss]ources?', '[Cc]leanup[ -]?[Cc]ite', '[Cc]leanup[ -]?[Vv]erify', '[Ff]ew ?[Rr]efs?', '[Ff]ew ?sources?', '[Ii]mprove[ -]?refs?', '[Ii]mprove[ -]?sources?', '[Mm][Cc][Nn]', '[Mm][Oo][Rr][Ee] ?[Cc][Nn]', '[Mm]issing ?[Cc]itations', '[Mm]issing ?[Rr]efs?', '[Mm]ore ?[Cc]itations', '[Mm]ore ?ref', '[Mm]ore ?[Ss]ources?', '[Nn]o ?sources', '[Nn]ot ?verified', '[Nn]o ?refs?', '^[Nn][Rr]', '[Rr]ef[ -]?[Ii]mprove', '[Rr]eference improve', '[Rr]eferences?', '[Rr]efs ?[Nn]eeded', '[Rr]eferenced', '[Rr]efim', '[Rr]ip', '[Ss]ources?', '[Uu]ncited[ -]?[Aa]rticle', '[Uu]nderreferenced', '[Uu][Nn][Rr][Ee]?[Ff]?', '[Uu]nsourced', '[Uu]nverified', '[Vv]erification', '[Vv]erify',

        'POV', '[Nn]pov', '[Pp]OV check', '[Pp]ov', '[Pp]ov check', '[Nn]POV', '[Nn]eutrality', '[Pp]OV-check-section', '[Pp]oint Of View', '[Pp]OV Check', '[Nn]POV Check', '[Nn]POV check', '[Pp]ov-Check', '[Pp]OV-Check', '[Pp]ov-check', '[Pp]ovcheck', '[Pp]OVCheck', '[Pp]OVcheck', '[Pp]ov Check', '[Pp]oV', '[Nn]eutral', '[Pp]ov-check-section', '[Nn]POV-dispute', '[Pp]OV dispute', '[Tt]oo friendly', '[Ww]hite washed', '[Pp]ov problem', '[Ss]pin', '[Nn]ot neutral', '[Pp]OV-check', '[Nn]PoV', '[Pp]oint of view']

print(regexcompare.compareSet(compareList,False))