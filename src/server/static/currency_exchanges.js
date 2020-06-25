function update_btc_usdt_currency_exchanges_graph() {
    $.getJSON("http://localhost:8000/currency-exchanges", plot);
}


document.addEventListener("DOMContentLoaded", function(event) {
    update_btc_usdt_currency_exchanges_graph();
});
