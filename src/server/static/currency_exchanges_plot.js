function plot(currency_exchanges) {
    var graphDocument = document.getElementById('graph');

    layout = {
        title: 'BTC-USDT',
        xaxis: {
            title: 'Date time (UTC)',
        },
    };

    high_trace = {
        y: currency_exchanges.map(currency_exchange => currency_exchange.high),
        x: currency_exchanges.map(currency_exchange => currency_exchange.updated_at),
        name: 'High',
        type: 'scatter',
    };

    low_trace = {
        y: currency_exchanges.map(currency_exchange => currency_exchange.low),
        x: currency_exchanges.map(currency_exchange => currency_exchange.updated_at),
        name: 'Low',
        type: 'scatter',
    };

    data = [high_trace, low_trace];

    Plotly.react(graphDocument, data, layout);
}
