function addRowHandlers(laCellule) {
    //alert("La valeur de la case: " + laCellule.innerHTML);
    
    var w = window.open('new_page.php', 'windowname');
    w.onload = function() {
    	//dans cette fonction tu peux modifier la page new_page comme tu veux avec les informations que tu veux
         w.document.getElementById("beautitre").innerHTML=laCellule.innerHTML;
     }
    w.document.close();
}
