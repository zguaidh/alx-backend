import { createClient, print } from 'redis';

const client = createClient();

client.on('connect', function() {
  console.log('Redis client connected to the server');
});

client.on('error', function(err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, print);
  
}

const get = promisify(client.get).bind(client);

async function displaySchoolValue(schoolName){
  try {
    const result = await get(schoolName);
    console.log(result);
  } catch (err) {
      console.error(err);
  }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
