const express = require('express');
const fs = require('fs');
const csv_parser = require('csv-parser');

const app = express();
const port = 3000;

app.get('/data/:stock_exchange/:symbol', async (req, res) => {
  const { symbol } = req.params;
  const { stock_exchange } = req.params;

  const csvFilePath = `./data/${stock_exchange}/${symbol}.csv`;

  res.setHeader('Content-Type', 'application/json');

  const data = [];

  const getCurrentTimeISO = () => {
    return new Date().toISOString();
  };

  fs.createReadStream(csvFilePath)
    .pipe(csv_parser())
    .on('data', (row) => {
      data.push(row);
    })
    .on('end', async () => {
      for (const row of data) {

        row.timestamp = getCurrentTimeISO();
        res.write(JSON.stringify(row) + '\n');

        await new Promise((resolve) => setTimeout(resolve, 2000));
      }

      res.end();
    });
});


app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
