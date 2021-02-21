var tr = document.getElementsByClassName("cmc-table table___1p4Jy")[0].getElementsByTagName("tbody")[0].getElementsByTagName("tr");
var data = "";
for(let i=0; i<tr.length; ++i){
data = data + tr[i].innerText + "\n";
}
console.log(data);

//https://coinmarketcap.com/currencies/bitcoin/historical-data/
