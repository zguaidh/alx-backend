import { createClient } from "redis";
import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';

const client = createClient();



client.on('connect', function() {
  console.log('Redis client connected to the server');
});

client.on('error', function(err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

const get = promisify(client.get).bind(client);

function reserveSeat(number) {
  client.set('available_seats',number);
}

async function getCurrentAvailableSeats() {
  const seats = await get('available_seats');
  // console.log(seats);
  return seats;
}


let reservationEnabled = true;
const queue = createQueue();

const app = express();

app.get('/available_seats', async function(req, res) {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({'numberOfAvailableSeats': availableSeats});
})

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ "status": "Reservation are blocked" });
    return;
  }
  
  const jobData = {'seat': 1};
  const job = queue.create('reserve_seat', jobData).save((error) => {
    if (error) {
      res.json({ "status": "Reservation failed" });
      return;
    }
  });
    res.json({"status": "Reservation in process"});
    job.on('complete', function (){
      console.log(`Seat reservation job ${job.id} completed`);
    });
    job.on('failed', function (error){
      console.log(`Seat reservation job ${job.id} failed: ${error}`);
    });
  });

app.get('/process', async function(req, res) {
  res.json({ "status": "Queue processing" });
  queue.process('reserve_seat', async function(job, done) {
    let seatsLeft = Number( await getCurrentAvailableSeats() );
    console.log(seatsLeft);
  
    if (seatsLeft === 0) {
      reservationEnabled = false;
      done(Error('Not enough seats available'));
    } else {
      reserveSeat(seatsLeft - 1);
      done();
    }
  });
});
reserveSeat(50);
app.listen(1245);