(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[0],{214:function(e,t,r){},215:function(e,t,r){},255:function(e,t,r){},256:function(e,t,r){"use strict";r.r(t);var n=r(268),a=r(140),c=r(0),s=r.n(c),i=r(14),l=r(51),o=r(269),u=r(91),j=r(133),d=r(92),b=r.n(d);function h(){return(h=Object(j.a)(Object(u.a)().mark((function e(){var t;return Object(u.a)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,b.a.get("api/ghost/list");case 2:return t=e.sent,console.log("get structure list in api"),console.log(t),e.abrupt("return",t.data);case 6:case"end":return e.stop()}}),e)})))).apply(this,arguments)}b.a.defaults.xsrfHeaderName="X-CSRFToken";var p=r(74),O=r(2),x=function(){return Object(O.jsx)(o.a.Body,{className:"flex-container",children:Object(O.jsx)(p.a,{className:"spinner-size"})})},f=r(55),g=r(13),m=r(263),v=r(39),y=r(271),w=r(40),S=r(90),C=r(264),F=r(265),P=r(266),N=r(136),H=r(270),L=r(267),z=(r(214),r(215),function(){return Object(O.jsx)(o.a.Body,{className:"flex-container",children:Object(O.jsxs)("div",{className:"text-center",children:[Object(O.jsx)("div",{className:"error-size bottom-text",children:Object(O.jsxs)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"100",height:"100",fill:"currentColor",class:"bi bi-exclamation-triangle error-anim",viewBox:"0 0 16 16",children:[Object(O.jsx)("path",{d:"M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.146.146 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.163.163 0 0 1-.054.06.116.116 0 0 1-.066.017H1.146a.115.115 0 0 1-.066-.017.163.163 0 0 1-.054-.06.176.176 0 0 1 .002-.183L7.884 2.073a.147.147 0 0 1 .054-.057zm1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566z"}),Object(O.jsx)("path",{d:"M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995z"})]})}),Object(O.jsx)("h3",{className:"text-margin",children:"Error Loading Component"})]})})});var k={option:function(e){return Object(g.a)(Object(g.a)({},e),{},{color:"black"})}};function R(e){var t=e.message;return Object(O.jsx)(m.a,{id:"character_tooltip",children:t})}function B(e){var t=e.column;t.filterValue,t.preFilteredRows,t.setFilter;return Object(O.jsx)(O.Fragment,{})}function D(e){var t=e.column,r=t.filterValue,n=t.preFilteredRows,a=t.setFilter,c=n.length;return Object(O.jsx)("input",{className:"form-control",value:r||"",onChange:function(e){a(e.target.value||void 0)},placeholder:"Search ".concat(c," records...")})}function M(e){var t=e.column,r=t.setFilter,n=t.filterValue,a=t.preFilteredRows,c=t.id,i=s.a.useMemo((function(){var e=new Set;return a?(a.forEach((function(t){null!==t.values[c]&&("object"===typeof t.values[c]?e.add(t.values[c].name):e.add(t.values[c]))})),Object(f.a)(e.values())):[]}),[c,a]);return Object(O.jsx)(S.a,{title:n,onChange:function(e){return r(e.value)},value:{label:n||"All"},defaultValue:{label:"All"},styles:k,options:[{id:-1,value:"",label:"All"}].concat(i.map((function(e,t){return{id:t,value:e,label:e}})))},n)}var E=function(){return{}};var T=function(e){var t=e.isLoading,r=e.isFetching,n=e.data,a=e.error,c=e.columns,i=e.asyncExpandFunction,l=e.getRowProps,o=void 0===l?E:l,u=s.a.useMemo((function(){return{Filter:B}}),[]),j=s.a.useMemo((function(){return{text:function(e,t,r){return e.filter((function(e){return t.some((function(t){if(r){var n=e.values[t];return"object"===typeof n&&(n=n.name),e.hasOwnProperty("originalSubRows")&&(n+=e.originalSubRows.reduce((function(e,r){return e+" "+(n=r,t.split(".").reduce((function(e,t){return e[t]}),n));var n}),"")),!!n&&n.toLowerCase().includes(r.toLowerCase())}return!0}))}))}}}),[]),d=Object(w.useTable)({columns:c,data:n,defaultColumn:u,filterTypes:j,initialState:{pageSize:20}},w.useFilters,w.useSortBy,w.useExpanded,w.usePagination),b=d.getTableProps,h=d.getTableBodyProps,x=d.headerGroups,f=d.page,m=d.prepareRow,S=d.canPreviousPage,k=d.canNextPage,D=d.pageOptions,M=d.pageCount,T=d.gotoPage,A=d.nextPage,V=d.previousPage,_=d.setPageSize,G=d.visibleColumns,J=d.state,Q=J.pageIndex,I=J.pageSize;return t?Object(O.jsx)("div",{className:"col-xs-12 text-center",children:Object(O.jsx)(p.a,{className:"spinner-size"})}):a?Object(O.jsx)(z,{}):Object(O.jsxs)(O.Fragment,{children:[Object(O.jsxs)(C.a,{striped:!0,children:[Object(O.jsxs)("thead",Object(g.a)(Object(g.a)({},b()),{},{children:[x.map((function(e){return Object(O.jsx)("tr",Object(g.a)(Object(g.a)({},e.getHeaderGroupProps()),{},{children:e.headers.map((function(e){return Object(O.jsxs)("th",Object(g.a)(Object(g.a)({},e.getHeaderProps(e.getSortByToggleProps())),{},{children:[e.render("Header"),Object(O.jsx)("span",{className:"pull-right",children:e.canSort?e.isSorted?e.isSortedDesc?Object(O.jsx)(F.a,{glyph:"sort-by-attributes-alt"}):Object(O.jsx)(F.a,{glyph:"sort-by-attributes"}):Object(O.jsx)(F.a,{glyph:"sort"}):""})]}))}))}))})),x.map((function(e){return Object(O.jsx)("tr",Object(g.a)(Object(g.a)({},e.getHeaderGroupProps()),{},{children:e.headers.map((function(e){return Object(O.jsx)("th",Object(g.a)(Object(g.a)({},e.getHeaderProps()),{},{children:Object(O.jsx)("div",{children:e.canFilter?e.render("Filter"):null})}))}))}))}))]})),Object(O.jsx)("tbody",Object(g.a)(Object(g.a)({},h()),{},{children:f.map((function(e,t){m(e);var r=o(e);return Object(O.jsxs)(O.Fragment,{children:[Object(O.jsx)("tr",Object(g.a)(Object(g.a)({},e.getRowProps(r)),{},{children:e.cells.map((function(e){return Object(O.jsx)("td",Object(g.a)(Object(g.a)({style:{verticalAlign:"middle"}},e.getCellProps()),{},{children:e.render("Cell")}))}))})),e.isExpanded&&i({row:e,rowProps:r,visibleColumns:G})]})}))}))]}),Object(O.jsx)("div",{className:"pagination pull-right",children:Object(O.jsxs)(P.a,{children:[Object(O.jsxs)(N.a,{children:[Object(O.jsx)(v.a,{bsStyle:"success",onClick:function(){return T(0)},disabled:!S,children:Object(O.jsx)(F.a,{glyph:"step-backward"})})," ",Object(O.jsx)(v.a,{bsStyle:"success",onClick:function(){return V()},disabled:!S,children:Object(O.jsx)(F.a,{glyph:"triangle-left"})})," ",Object(O.jsx)(v.a,{bsStyle:"success",onClick:function(){return A()},disabled:!k,children:Object(O.jsx)(F.a,{glyph:"triangle-right"})})," ",Object(O.jsx)(v.a,{bsStyle:"success",onClick:function(){return T(M-1)},disabled:!k,children:Object(O.jsx)(F.a,{glyph:"step-forward"})})]}),Object(O.jsxs)(N.a,{children:[Object(O.jsx)(v.a,{active:!0,bsStyle:"success",children:"Page Size:"})," ",Object(O.jsx)(H.a,{id:"pageSizeDropdown",bsStyle:"success",title:I,onSelect:function(e){_(Number(e))},children:[20,50,100,1e6].map((function(e){return Object(O.jsxs)(L.a,{id:e,eventKey:e,value:e,children:["Show ",e]},e)}))})]})]})}),Object(O.jsx)("div",{className:"pagination pull-left",children:Object(O.jsxs)(N.a,{children:[Object(O.jsx)(v.a,{active:!0,bsStyle:"info",children:Object(O.jsx)(O.Fragment,{children:D.length>0?Object(O.jsxs)(O.Fragment,{children:["Page"," ",Object(O.jsxs)("strong",{children:[Q+1," of ",D.length]})]}):Object(O.jsxs)(O.Fragment,{children:["Page ",Object(O.jsx)("strong",{children:"- of -"})]})})})," ",r?Object(O.jsx)(y.a,{placement:"bottom",overlay:R({message:"Refreshing Data"}),children:Object(O.jsx)(v.a,{bsStyle:"info",children:Object(O.jsx)(F.a,{className:"glyphicon-refresh-animate",glyph:"refresh"})})}):Object(O.jsx)(y.a,{placement:"bottom",overlay:R({message:"Data Loaded: "+(new Date).toLocaleString()}),children:Object(O.jsx)(v.a,{bsStyle:"info",children:Object(O.jsx)(F.a,{glyph:"ok"})})})]})})]})},A=function(){var e=Object(l.useQuery)(["dashboard"],(function(){return function(){return h.apply(this,arguments)}()})),t=e.isLoading,r=e.error,n=e.data,a=e.isFetching,c=s.a.useMemo((function(){return[{Header:"Character",accessor:"char.name",Filter:D,filter:"text",Cell:function(e){return Object(O.jsx)("div",{style:{whiteSpace:"nowrap"},children:e.value})}},{Header:"Main",accessor:"main.name",Filter:D,filter:"text",Cell:function(e){return Object(O.jsx)("div",{style:{whiteSpace:"nowrap"},children:e.value})}},{Header:"Corp",accessor:"main.corp",Filter:M,filter:"text",Cell:function(e){return Object(O.jsx)("div",{style:{whiteSpace:"nowrap"},children:e.value})}},{Header:"Location",accessor:"location.name",Filter:M,filter:"text",Cell:function(e){return Object(O.jsx)("div",{style:{whiteSpace:"nowrap"},children:e.value})}},{Header:"Ship",accessor:"ship.name",Filter:M,filter:"text",Cell:function(e){return Object(O.jsx)("div",{style:{whiteSpace:"nowrap"},children:e.value})}},{Header:"Death Clone",accessor:"death_clone.name",Filter:M,filter:"text",Cell:function(e){return Object(O.jsx)("div",{style:{whiteSpace:"nowrap"},children:e.value})}},{Header:"Last Online",accessor:"logoff_date",Cell:function(e){return Object(O.jsx)("div",{style:{whiteSpace:"nowrap"},children:e.value})}},,{Header:"Join Date",accessor:"start_date",Cell:function(e){return Object(O.jsx)("div",{style:{whiteSpace:"nowrap"},children:e.value})}}]}),[]);return t?Object(O.jsx)(x,{}):r?Object(O.jsx)(z,{}):Object(O.jsx)(o.a.Body,{children:Object(O.jsx)(T,{isLoading:t,data:n,columns:c,error:r,isFetching:a})})};r(255);n.a.addDefaultLocale(a);var V=new l.QueryClient,_=function(){return Object(O.jsx)(l.QueryClientProvider,{client:V,children:Object(O.jsx)(A,{})})},G=document.getElementById("root");Object(i.render)(Object(O.jsx)(_,{}),G)}},[[256,1,2]]]);
//# sourceMappingURL=main.781f6650.chunk.js.map