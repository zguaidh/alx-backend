import  express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const listProducts = [
  { 'itemId': 1, 'itemName': 'Suitcase 250', 'price': 50, 'initialAvailableQuantity': 4},
  { 'itemId': 2, 'itemName': 'Suitcase 450', 'price': 100, 'initialAvailableQuantity': 10},
  { 'itemId': 3, 'itemName': 'Suitcase 650', 'price': 350, 'initialAvailableQuantity': 2},
  { 'itemId': 4, 'itemName': 'Suitcase 1050', 'price': 550, 'initialAvailableQuantity': 5}
];

function getItemById(id) {
  return listProducts.find(product => product.itemId === id)
}

const app = express();

app.listen(1245);

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

const client = createClient();

client.on('connect', function() {
  console.log('Redis client connected to the server');
});

client.on('error', function(err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

function reserveStockById(itemId, stock) {
  client.set(itemId, stock);
}

const get = promisify(client.get).bind(client);

async function getCurrentReservedStockById(itemId) {
  const stock = await get(itemId);
  return stock;
}



app.get('/list_products/:itemId', async function (req, res) {
  const itemId = req.params.itemId;
  const item = getItemById(parseInt(itemId));
  if (item) {
  const currentQuantity = await getCurrentReservedStockById(itemId);
  res.json({
    'itemId': item.itemId,
    'itemName': item.itemName,
    'price': item.price,
    'initialAvailableQuantity': item.initialAvailableQuantity,
    'currentQuantity': currentQuantity !== null ? parseInt(currentQuantity) : item.initialAvailableQuantity
  });
} else {
  res.json({'status': 'Product not found'});
}
});

app.get('/reserve_product/:itemId', async function (req, res) {
  const itemId = req.params.itemId;
  const item = getItemById(parseInt(itemId));

  if (!item) {
    res.json({'status': 'Product not found'});
    return;
  }

  let currentStock = await getCurrentReservedStockById(itemId);
  if (currentStock) {
    currentStock = parseInt(currentStock);
  
    if (currentStock <= 0) {
      
      res.json({'status': 'Not enough stock available', 'itemId': parseInt(itemId)});
    } else {
      reserveStockById(itemId, currentStock - 1); 
      res.json({"status":"Reservation confirmed","itemId": item.itemId});
    } 
  } else {
    reserveStockById(item.itemId, item.initialAvailableQuantity - 1);
    res.json({"status":"Reservation confirmed","itemId": item.itemId});
  }
});