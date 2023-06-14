let arbol_ast = "" ;
let reporte_errores = "" ;
let reporte_simbolos = "" ;

$("#bt_analizar").click(function () {
  let code = editor.getValue();
  //console.log($("#area_editor").val());
  console.log(editor.getValue());
  console.log("-----------------------");
  
$.post("http://127.0.0.1:5000/execute",
{
  code: code,
},
function(data, status){
     
  //console.log(data.arbol.listaIns.length);
  console.log(data);
  //console.log(data.consola)

  //var expresiones = "";

  // for (var i = 0; i < data.arbol.listaIns.length; i++) {
      
  //   if (data.arbol.listaIns[i].expresion.valor){
  //     expresiones += data.arbol.listaIns[i].expresion.valor + "\n";
  //   }
  //   console.log(data.arbol.listaIns[i]);
    
    
  // }
  console.log("-----------------------");
  //console.log(expresiones);
  console.log("xd")
  console.log("-----------------------");
  //consola.setValue(data.consola);

  if(data.result == "ok"){
      console.log("Si funciona el back uwu")

  }
  consola.setValue(data.result)

  if (data.flag === "True"){
    simbolos_(data.tablaSimbolos)
    AST_(data.astBase64)
    arbol_ast = data.astBase64;
    reporte_simbolos = data.tablaSimbolos
  } else{
    errores_(data.listaErrores)
    reporte_errores = data.listaErrores;
  }

  console.log("Proceso terminado..")

});
})

$("#bt_limpiar").click(function () {
    editor.setValue("");
    consola.setValue("");
})


function AST_(ImageBase64) {
  var a = document.createElement("a"); 
  a.href = "data:image/png;base64," + ImageBase64;  
  a.download = "ReporteAST.png";  
  a.click();  
  }


 


function errores_(listaErrores) {
alert("Mensaje: Generando Reporte Errores.." + "\nEstado: En proceso.");
//alert(listaErrores)
var tablaerrores = getErrores(listaErrores)
console.log(tablaerrores)
download(tablaerrores,"ReporteErrores.html","text/html")
}

function simbolos_(listaSimbolos) {
alert("Mensaje: Generando Reporte Simbolos .." + "\nEstado: En proceso.");
//alert(listaSimbolos)

var tablasimbolos = getSimbolos(listaSimbolos)

console.log(tablasimbolos)

download(tablasimbolos,"ReporteSimbolos.html","text/html")

}

function getErrores(listaErrores){
  var texto="";
  
  texto+=`<html><head><title>Reporte de Tabla de Simbolos</title><style>
  table {
    border-collapse: collapse;
    width: 100%;
  }
  
  th, td {
    text-align: left;
    padding: 8px;
  }
  
  tr:nth-child(even){background-color: #f2f2f2}
  
  th {
    background-color: #ed0000;
    color: white;
  }
  </style></head><body>
  <h1>Reporte de Errores</h1>
  <table>
  <tr>
      <th>No.</th>
      <th>Tipo de Error</th>
      <th>Descripción</th>
      <th>Linea</th>
      <th>Columna</th>

   
  </tr>`;
  var cuenta=1;
  listaErrores.forEach(error =>{
      texto+="<tr>\n";
      texto+="<td>"+cuenta+"</td>\n";
      texto+="<td>"+error.tipo+"</td>\n";
      texto+="<td>"+error.descripcion+"</td>\n";
      texto+="<td>"+error.linea+"</td>\n";
      texto+="<td>"+error.columna+"</td>\n";
      texto+="</tr>";
      cuenta++;
  })
  texto+="</table></body></html>";
  
  return texto;
  
  }  

function getSimbolos(listaSimbolos){
var texto="";

texto+=`<html><head><title>Reporte de Tabla de Simbolos</title><style>
table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  text-align: left;
  padding: 8px;
}

tr:nth-child(even){background-color: #f2f2f2}

th {
  background-color: #4CAF50;
  color: white;
}
</style></head><body>
<h1>Reporte de Tabla de Simbolos</h1>
<table>
<tr>
    <th>No.</th>
    <th>Identificador</th>
    <th>Tipo de Simbolo</th>
    <th>Tipo de Variable</th>
    <th>Columna</th>
    <th>Linea</th>
 
</tr>`;
var cuenta=1;
listaSimbolos.forEach(simbolo =>{
    texto+="<tr>\n";
    texto+="<td>"+cuenta+"</td>\n";
    texto+="<td>"+simbolo.identificador+"</td>\n";
    texto+="<td>"+simbolo.tipoSimbolo+"</td>\n";
    texto+="<td>"+simbolo.tipoVar+"</td>\n";
    texto+="<td>"+simbolo.columna+"</td>\n";
    texto+="<td>"+simbolo.linea+"</td>\n";
    texto+="</tr>";
    cuenta++;
})
texto+="</table></body></html>";

return texto;

}  

  
function download(text, name, type) {
  var a = document.createElement('a');
 
  var file = new Blob([text], {type: type});
  a.href = URL.createObjectURL(file);
  a.download = name;
  a.click();
  a.remove();

}

function clickElem(elem) {
var eventMouse = document.createEvent("MouseEvents")
eventMouse.initMouseEvent("click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
elem.dispatchEvent(eventMouse)
}

function abrir_() {
readFile = function(e) {
  var file = e.target.files[0];
  if (!file) {
    return;
  }
  var reader = new FileReader();
  reader.onload = function(e) {
    var contents = e.target.result;
    //$("#area_editor").val(contents);
    editor.setValue(contents);
    document.body.removeChild(fileInput)
  }
  reader.readAsText(file)
}
fileInput = document.createElement("input")
fileInput.type='file'
fileInput.style.display='none'
fileInput.onchange=readFile

document.body.appendChild(fileInput)
clickElem(fileInput)
}


function guardar_(){

var contador_guardados = 0;

var text = editor.getValue();
var filename = "DocumentoGuardado_"+contador_guardados+".cst";

contador_guardados = contador_guardados +1;

var element = document.createElement('a');
element.setAttribute('href','data:text/plain;charset=utf-8, ' + encodeURIComponent(text));
element.setAttribute('download', filename);
document.body.appendChild(element);
element.click();

}

function nuevo_(){
//$("#area_editor").val("");
//$("#area_consola").val("");
editor.setValue("");
consola.setValue("");
}