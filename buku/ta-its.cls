\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ta-its}[2011/12/23 My Class]
\LoadClass[11pt,a5paper,twoside]{book}
\RequirePackage[tmargin=2.5cm,bmargin=2.5cm,lmargin=2.5cm,rmargin=2.0cm]{geometry}
\RequirePackage{fontspec}
    \setsansfont{Trebuchet MS}
    \setmainfont[Scale=1.025]{Times New Roman}
    \setmonofont[Scale=0.9]{Courier New}
\RequirePackage{tocbibind}
\RequirePackage[boxruled]{algorithm2e}
\SetAlFnt{\scriptsize}
\SetAlCapFnt{\scriptsize}
\SetAlCapNameFnt{\scriptsize}

\makeatletter
\renewcommand{\algocf@caption@boxruled}{%
	\hrule
	\hbox to \hsize{%
		\vrule\hskip-0.4pt
		\vbox{   
			\vskip\interspacetitleboxruled%
			\unhbox\algocf@capbox\hfill
			\vskip\interspacetitleboxruled
		}%
		\hskip-0.4pt\vrule%
	}\nointerlineskip%
}%
\makeatother

\newenvironment{prosedur}[1][htb]
{\renewcommand{\algorithmcfname}{Prosedur}% Update algorithm name
	\begin{algorithm}[#1]%
	}{\end{algorithm}}

\RequirePackage{graphicx}
\RequirePackage{eso-pic}
\RequirePackage[bahasa]{babel}

%Set justify text without hyphenation
\tolerance=1
\emergencystretch=\maxdimen
\hyphenpenalty=10000
\hbadness=10000

% JSON
\usepackage{listings}
\usepackage{xcolor}

\colorlet{punct}{red!60!black}
\definecolor{background}{HTML}{EEEEEE}
\definecolor{delim}{RGB}{20,105,176}
\colorlet{numb}{magenta!60!black}

\lstdefinelanguage{json}{
	frame=single,
	tabsize=2,
    basicstyle=\normalfont\ttfamily,
    numbers=left,
    numberstyle=\scriptsize,
    stepnumber=1,
    numbersep=8pt,
    showstringspaces=false,
    breaklines=true,
    backgroundcolor=\color{background},
    literate=
     *{0}{{{\color{numb}0}}}{1}
      {1}{{{\color{numb}1}}}{1}
      {2}{{{\color{numb}2}}}{1}
      {3}{{{\color{numb}3}}}{1}
      {4}{{{\color{numb}4}}}{1}
      {5}{{{\color{numb}5}}}{1}
      {6}{{{\color{numb}6}}}{1}
      {7}{{{\color{numb}7}}}{1}
      {8}{{{\color{numb}8}}}{1}
      {9}{{{\color{numb}9}}}{1}
      {:}{{{\color{punct}{:}}}}{1}
      {,}{{{\color{punct}{,}}}}{1}
      {\{}{{{\color{delim}{\{}}}}{1}
      {\}}{{{\color{delim}{\}}}}}{1}
      {[}{{{\color{delim}{[}}}}{1}
      {]}{{{\color{delim}{]}}}}{1},
}

\usepackage[titles]{tocloft}
\renewcommand{\cftchappresnum}{BAB }
\cftsetindents{chapter}{0in}{0.575in}

%Indent first paragraph
\usepackage{indentfirst}

\RequirePackage{enumitem}
    \setlist{nolistsep}
\RequirePackage{array,etoolbox}
    \preto\tabular{\setcounter{magicrownumbers}{0}}
    \preto\longtable{\setcounter{magicrownumbers}{0}}
    \preto\tabularx{\setcounter{magicrownumbers}{0}}
    \preto\tabulary{\setcounter{magicrownumbers}{0}}
    \newcounter{magicrownumbers}
    \newcommand\rownumber{\stepcounter{magicrownumbers}\arabic{magicrownumbers}}

\RequirePackage{setspace}
    \singlespacing
\RequirePackage{fancyhdr}
    \fancyhf{}
    \renewcommand{\headrulewidth}{0pt}
	\fancypagestyle{front}{%
		\fancyhf{}
		\cfoot{\thepage}
	}
	\fancypagestyle{main}{%
		\fancyhf{}
		\lhead[\thepage]{}
		\rhead[]{\thepage}
	}

\makeatletter
\renewcommand\frontmatter{%
	\cleardoublepage
	\@mainmatterfalse
	\pagestyle{front}
	\pagenumbering{roman}}

\renewcommand\mainmatter{%
	\cleardoublepage
	\@mainmattertrue
	\pagestyle{main}
	\pagenumbering{arabic}}
\makeatother
    
\RequirePackage[hypcap=true, font=footnotesize]{caption}
    \captionsetup{labelfont=bf, justification=centering, singlelinecheck=false, format=plain}

\RequirePackage{tabulary, booktabs, longtable, ltcaption, ltabptch}
\RequirePackage[referable]{threeparttablex}

%% define a new envrionment which marries longtable with tabulary
% from http://tex.stackexchange.com/questions/78075/multi-page-with-tabulary (see there for usage)
% with modifications taken from the ltxtable package to make captions work
\makeatletter
\newcommand*\TY@cap@gobble[2][]{\\}% from ltxtable (adjusted)
\def\ltabulary{%
    \def\caption{% from ltxtable (adjusted)
        \@ifstar\TY@cap@gobble\TY@cap@gobble}
    \def\endfirsthead{\\}%
    \def\endhead{\\}%
    \def\endfoot{\\}%
    \def\endlastfoot{\\}%
    \def\tabulary{%
        \def\TY@final{%
    \def\endfirsthead{\LT@end@hd@ft\LT@firsthead}%
    \def\endhead{\LT@end@hd@ft\LT@head}%
    \def\endfoot{\LT@end@hd@ft\LT@foot}%
    \def\endlastfoot{\LT@end@hd@ft\LT@lastfoot}%
    \longtable}%secnumdepth
        \let\endTY@final\endlongtable
        \TY@tabular}%
    \dimen@\columnwidth
    \advance\dimen@-\LTleft
    \advance\dimen@-\LTright
    \tabulary\dimen@}
\def\endltabulary{\endtabulary}
\makeatother

\RequirePackage{titlesec}
	\setcounter{secnumdepth}{3}
    \titleformat{\chapter}[display]{\filcenter\fontsize{11}{11}\bfseries}{\chaptername \ \thechapter}{11pt}{\filcenter\fontsize{11}{11}\bfseries\uppercase}
   	\titlespacing*{\chapter}{0pt}{-50pt}{20pt}
    %\titlespacing*{\section}{0pt}{11pt}{0pt}
    %\titlespacing*{\subsection}{0pt}{11pt}{0pt}
    %\titlespacing*{\subsubsection}{0pt}{11pt}{0pt}
    \titleformat*{\section}{\fontsize{11}{11}\bfseries}
    \titleformat*{\subsection}{\fontsize{11}{11}\bfseries}
    \titleformat*{\subsubsection}{\fontsize{11}{11}\bfseries}

\addto\captionsbahasa{%
	\renewcommand\bibname{DAFTAR PUSTAKA}%
	\renewcommand\contentsname{DAFTAR ISI}%
	\renewcommand\listtablename{DAFTAR TABEL}%
	\renewcommand\listfigurename{DAFTAR GAMBAR}%
	\renewcommand{\chaptername}{BAB}
}%

\renewcommand*\thechapter{\Roman{chapter}}
\renewcommand{\thesection}{\arabic{chapter}.\arabic{section}}
\renewcommand{\thesubsection}{\arabic{chapter}.\arabic{section}.\arabic{subsection}}
\newcommand{\pic}{Gambar}
\newcommand{\tab}{Tabel}
\newcommand{\code}{Kode}
\renewcommand{\thefigure}{\arabic{chapter}.\arabic{figure}}
\renewcommand{\thetable}{\arabic{chapter}.\arabic{table}}

\newcommand{\judul}{}
\newcommand{\kodeTA}{}
\newcommand{\judulEnglish}{}
\newcommand{\penulis}{}
\newcommand{\nrp}{}
\newcommand{\gelar}{}
\newcommand{\jurusan}{}
\newcommand{\jurusanEnglish}{}
\newcommand{\fakultas}{}
\newcommand{\fakultasSingkatan}{}
\newcommand{\fakultasEnglish}{}
\newcommand{\prodi}{}
\newcommand{\bidangStudi}{}
\newcommand{\pembimbingSatu}{}
\newcommand{\nipPembimbingSatu}{}
\newcommand{\pembimbingDua}{}
\newcommand{\nipPembimbingDua}{}
\newcommand{\tahun}{\monthnamebahasa}
\newcommand{\bulan}{}

% Empty Even Page
\makeatletter
\def\emptypage@emptypage{%
     \begin{center}
     \emph{(Halaman ini sengaja dikosongkan)}
     \end{center}
     \newpage%    
}%
\def\cleardoublepage{%
        \clearpage%
        \if@twoside%
            \ifodd\c@page%
                % do nothing
            \else%
                \emptypage@emptypage%
            \fi%
        \fi%
}%
\makeatother

% Custom \title, \author, \institution
\renewcommand{\title}[3]{%
\renewcommand{\judul}{#1}%
\renewcommand{\judulEnglish}{#2}%
\renewcommand{\kodeTA}{#3}%
}%

\renewcommand{\author}[2]{%
\renewcommand{\penulis}{#1}%
\renewcommand{\nrp}{#2}%
}%

\newcommand{\supervisorOne}[2]{
\renewcommand{\pembimbingSatu}{#1}%
\renewcommand{\nipPembimbingSatu}{#2}%
}

\newcommand{\supervisorTwo}[2]{
\renewcommand{\pembimbingDua}{#1}%
\renewcommand{\nipPembimbingDua}{#2}%
}

\newcommand{\degree}[8]{
\renewcommand{\gelar}{#1 }
\renewcommand{\bidangStudi}{#2 }
\renewcommand{\prodi}{#3 }
\renewcommand{\jurusan}{#4 }
\renewcommand{\jurusanEnglish}{#5 }
\renewcommand{\fakultas}{#6 }
\renewcommand{\fakultasSingkatan}{#7 }
\renewcommand{\fakultasEnglish}{#8 }
}

\renewcommand{\time}[2]{
\renewcommand{\bulan}{#1 }
\renewcommand{\tahun}{#2 }

}



\newpage
% Custom \maketitle
\makeatletter
\def\maketitle{%
% Set page number from first cover
\setcounter{page}{-1}
% Set page number position to bottom center
\pagestyle{fancy}
\fancyhead{}
\fancyfoot{}
\fancyfoot[C]{\thepage}
\newpage%
    \newgeometry{top=7cm,left=2cm,bottom=2cm}%
    \sffamily%
    \thispagestyle{empty}%
    \color{white}%
    { \noindent TUGAS AKHIR - \kodeTA }\\*[10pt]%
    {\large\textbf{\MakeUppercase{\judul}}} \\*[32pt]%
    \MakeUppercase{\penulis} \\*%
    NRP \nrp \\*[10pt]%
    Dosen Pembimbing I\\*%
    \pembimbingSatu \\*[10pt]%
    \ifdef{\pembimbingDua}{
        Dosen Pembimbing II\\*%
    	\pembimbingDua
    }{} \\*[32pt]%
    JURUSAN \MakeUppercase{\jurusan} \\*%
    Fakultas \fakultas \\*%
    Institut Teknologi Sepuluh Nopember \\*%
    Surabaya, \tahun \\*%
    \AddToShipoutPictureBG*{\includegraphics[width=\paperwidth,height=\paperheight]{img/sampul.png}}%
    \rmfamily%
    \normalsize%
    \restoregeometry%
    \color{black}%
    \cleardoublepage%
\newpage%
    \newgeometry{top=7cm,left=2cm,bottom=2cm}%
    \sffamily%
    { \noindent TUGAS AKHIR - \kodeTA }\\*[10pt]%
    {\large\textbf{\MakeUppercase{\judul}}} \\*[32pt]%
    \MakeUppercase{\penulis} \\*%
    NRP \nrp \\*[10pt]%
    Dosen Pembimbing I\\*%
    \pembimbingSatu \\*[10pt]%
    \ifdef{\pembimbingDua}{
        Dosen Pembimbing II\\*%
    	\pembimbingDua
    }{} \\*[10pt]%
    JURUSAN \MakeUppercase{\jurusan} \\*%
    Fakultas \fakultas \\*%
    Institut Teknologi Sepuluh Nopember \\*%
    Surabaya, \tahun \\*%
    \AddToShipoutPictureBG*{\includegraphics[width=\paperwidth,height=\paperheight]{img/sampulWhite.png}}%
    \rmfamily%
    \normalsize%
    \restoregeometry%
    \cleardoublepage%
\newpage%
    \newgeometry{top=7cm,left=2cm,bottom=2cm}%
    \sffamily%
    { \noindent UNDERGRADUATE THESIS - \kodeTA }\\*[10pt]%
    {\large\textbf{\MakeUppercase{\judulEnglish}}} \\*[32pt]%
    \MakeUppercase{\penulis} \\*%
    NRP \nrp \\*[10pt]%
    Supervisor I\\*%
    \pembimbingSatu \\*[10pt]%
    \ifdef{\pembimbingDua}{
        Supervisor II\\*%
    	\pembimbingDua
    }{} \\*[10pt]%
    Department of \MakeUppercase{\jurusanEnglish} \\*%
    Faculty of \fakultasEnglish \\*%
    Institut Teknologi Sepuluh Nopember \\*%
    Surabaya, \tahun \\*%
    \AddToShipoutPictureBG*{\includegraphics[width=\paperwidth,height=\paperheight]{img/sampulWhite.png}}%
    \rmfamily%
    \normalsize%
    \restoregeometry%
    \cleardoublepage%
}%
\makeatother

% lembarpengesahan
\makeatletter
\def\legalityPaper{%
\newpage%
    \begin{centering}%
    	\textbf{\large{LEMBAR PENGESAHAN}} \\*[10pt]%
        \textbf{\MakeUppercase{\judul}} \\*[10pt]%
        \textbf{\MakeUppercase{TUGAS AKHIR}} \\*%
        Diajukan Guna Memenuhi Salah Satu Syarat \\*%
        Memperoleh Gelar \gelar \\*%
        pada \\*%
        Bidang Studi \bidangStudi \\*%
        Program Studi \prodi  Jurusan \jurusan \\*%
        Fakultas \fakultas \\*%
        Institut Teknologi Sepuluh Nopember \\*[10pt]%
        Oleh : \\*%
        \textbf{\MakeUppercase{\penulis}} \\*%
        \textbf{NRP: \nrp} \\*[20pt]%
    \end{centering}%

    {\noindent Disetujui oleh Dosen Pembimbing Tugas Akhir :}\\*[15pt]         
    \pembimbingSatu \hfill \hfill ........................ \\ NIP: \nipPembimbingSatu \hfill \hfill (Pembimbing 1) \\*[15pt]%
    %
    \ifdef{\pembimbingDua}{{\noindent \pembimbingDua  \hfill \hfill .........................}  \\ NIP: \nipPembimbingDua \hfill \hfill (Pembimbing 2) \\*[20pt]}{}%

    \begin{centering}%
        \textbf{SURABAYA} \\*
        \textbf{\bulan \tahun} \\*%
    \end{centering}%
    \cleardoublepage%
}%
\makeatother

% Environment
% abstrak
\newenvironment{abstrak}{
\addcontentsline{toc}{chapter}{ABSTRAK}
\begin{centering}
\textbf{\MakeUppercase{\judul}} \\*[20pt]%
\end{centering}

\noindent\begin{tabular}{>{\bfseries}ll>{\bfseries}p{6.5cm}}
Nama  & :& \MakeUppercase{\penulis} \\
NRP & :& \nrp \\
Jurusan  & :& \jurusan \fakultasSingkatan \\
Pembimbing I  & :& \pembimbingSatu
\ifdef{\pembimbingDua}{\\Pembimbing II  & :& \pembimbingDua}{}
\end{tabular}
\\*[20pt]
\begin{centering}
\textbf{Abstrak} \\*[10pt]
\end{centering}
\begin{itshape}
}{\end{itshape}}

% abstract
\newenvironment{abstract}{
\addcontentsline{toc}{chapter}{ABSTRACT}
\begin{centering}
\textbf{\MakeUppercase{\judulEnglish}} \\*[20pt]%
\end{centering}

\noindent\begin{tabular}{>{\bfseries}ll>{\bfseries}p{6.5cm}}
Name  & :& \MakeUppercase{\penulis} \\
NRP & :& \nrp \\
Major  & :& \jurusanEnglish \fakultasSingkatan \\
Supervisor I  & :& \pembimbingSatu 
\ifdef{\pembimbingDua}{\\Supervisor II  & :& \pembimbingDua}{}
\end{tabular}
\\*[20pt]
\begin{centering}
\textbf{Abstract} \\*[10pt]
\end{centering}
\begin{itshape}
}{\end{itshape}}

\endinput