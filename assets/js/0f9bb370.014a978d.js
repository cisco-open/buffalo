"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[4],{365:(n,e,t)=>{t.r(e),t.d(e,{assets:()=>r,contentTitle:()=>a,default:()=>h,frontMatter:()=>l,metadata:()=>o,toc:()=>c});var s=t(4848),i=t(8453);const l={sidebar_position:3},a="Installation",o={id:"Getting-started/Installation",title:"Installation",description:"Installing Python Packages",source:"@site/docs/Getting-started/Installation.md",sourceDirName:"Getting-started",slug:"/Getting-started/Installation",permalink:"/buffalo/docs/Getting-started/Installation",draft:!1,unlisted:!1,editUrl:"https://github.com/cisco-open/buffalo/tree/main/docs/Getting-started/Installation.md",tags:[],version:"current",sidebarPosition:3,frontMatter:{sidebar_position:3},sidebar:"tutorialSidebar",previous:{title:"Why Buffalo?",permalink:"/buffalo/docs/Getting-started/why-buffalo"},next:{title:"Usage (Demos)",permalink:"/buffalo/docs/Getting-started/Usage"}},r={},c=[{value:"Installing Python Packages",id:"installing-python-packages",level:4},{value:"Installing Elasticsearch",id:"installing-elasticsearch",level:4},{value:"Installing Stanford CoreNLP",id:"installing-stanford-corenlp",level:4},{value:"Installing RANNET Model",id:"installing-rannet-model",level:4}];function d(n){const e={a:"a",blockquote:"blockquote",code:"code",em:"em",h1:"h1",h4:"h4",li:"li",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,i.R)(),...n.components};return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(e.h1,{id:"installation",children:"Installation"}),"\n",(0,s.jsx)(e.h4,{id:"installing-python-packages",children:"Installing Python Packages"}),"\n",(0,s.jsx)(e.p,{children:"To start, we can clone this repository using:"}),"\n",(0,s.jsx)(e.pre,{children:(0,s.jsx)(e.code,{children:"git clone https://github.com/cisco-open/BUFFALO.git\n"})}),"\n",(0,s.jsx)(e.p,{children:"Next, we must install the necessary packages for BUFFALO. For this, we have two options:"}),"\n",(0,s.jsxs)(e.blockquote,{children:["\n",(0,s.jsx)(e.p,{children:"Will have a conda env/requirements.txt coming soon!"}),"\n"]}),"\n",(0,s.jsx)(e.p,{children:"Need to pip install the following:"}),"\n",(0,s.jsxs)(e.ul,{children:["\n",(0,s.jsx)(e.li,{children:"streamlit"}),"\n",(0,s.jsx)(e.li,{children:"annotated_text"}),"\n",(0,s.jsx)(e.li,{children:"faiss"}),"\n",(0,s.jsx)(e.li,{children:"langchain"}),"\n",(0,s.jsx)(e.li,{children:"rannet"}),"\n",(0,s.jsx)(e.li,{children:"nltk"}),"\n",(0,s.jsx)(e.li,{children:"openie"}),"\n",(0,s.jsx)(e.li,{children:"elasticsearch"}),"\n",(0,s.jsx)(e.li,{children:"spacy"}),"\n"]}),"\n",(0,s.jsx)(e.p,{children:"\xa0 \xa0"}),"\n",(0,s.jsx)(e.h4,{id:"installing-elasticsearch",children:"Installing Elasticsearch"}),"\n",(0,s.jsxs)(e.p,{children:["Elasticsearch needs to be running in the background for the Output Verification component.\nPlease download Elasticsearch 8.9.0 at the following link ",(0,s.jsx)(e.a,{href:"https://www.elastic.co/downloads/elasticsearch",children:"Elasticsearch Download"})]}),"\n",(0,s.jsxs)(e.p,{children:["Next, ensure that security settings are disabled by going to ",(0,s.jsx)(e.code,{children:"Elasticsearch.yml"})," in the Elasticsearch installation folder and setting the following:"]}),"\n",(0,s.jsx)(e.pre,{children:(0,s.jsx)(e.code,{children:"xpack.security.enabled: false\nxpack.security.enrollment.enabled: false\n"})}),"\n",(0,s.jsx)(e.p,{children:(0,s.jsx)(e.a,{href:"https://discuss.elastic.co/t/disable-authentification-for-elasticsearch/304862/3",children:"More Info - Disabling Elasticsearch Security"})}),"\n",(0,s.jsx)(e.p,{children:"\xa0 \xa0"}),"\n",(0,s.jsx)(e.h4,{id:"installing-stanford-corenlp",children:"Installing Stanford CoreNLP"}),"\n",(0,s.jsxs)(e.blockquote,{children:["\n",(0,s.jsx)(e.p,{children:(0,s.jsx)(e.em,{children:(0,s.jsx)(e.strong,{children:"JAVA needs to be installed to run OpenIE!"})})}),"\n"]}),"\n",(0,s.jsxs)(e.p,{children:["Stanford CoreNLP also needs to be installed in order to run the Ouput Verification component.\nThe zip folder can be downloaded from ",(0,s.jsx)(e.a,{href:"https://stanfordnlp.github.io/CoreNLP/download.html",children:"Stanford OpenIE Repo"})]}),"\n",(0,s.jsx)(e.p,{children:"\xa0 \xa0"}),"\n",(0,s.jsx)(e.h4,{id:"installing-rannet-model",children:"Installing RANNET Model"}),"\n",(0,s.jsx)(e.p,{children:"Both RANNET base english model and model-store need to be downloaded. These can be found on the RANNET GitHub page."}),"\n",(0,s.jsx)(e.p,{children:"\xa0 \xa0"})]})}function h(n={}){const{wrapper:e}={...(0,i.R)(),...n.components};return e?(0,s.jsx)(e,{...n,children:(0,s.jsx)(d,{...n})}):d(n)}},8453:(n,e,t)=>{t.d(e,{R:()=>a,x:()=>o});var s=t(6540);const i={},l=s.createContext(i);function a(n){const e=s.useContext(l);return s.useMemo((function(){return"function"==typeof n?n(e):{...e,...n}}),[e,n])}function o(n){let e;return e=n.disableParentContext?"function"==typeof n.components?n.components(i):n.components||i:a(n.components),s.createElement(l.Provider,{value:e},n.children)}}}]);