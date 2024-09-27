module.exports = function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw Error(`Jobs is not an array`);
  }
  jobs.forEach((job) => {
    const jobQueue = queue.create('push_notification_code_3', job);
    jobQueue.save((err) => {
      if (!err) {
        console.log(`Notification job created: ${jobQueue.id}`);
      }
    });
    jobQueue.on('complete', function() {
      console.log(`Notification job ${jobQueue.id} completed`);
    }).on('failed', function(err) {
      console.log(`Notification job ${jobQueue.id} failed: ${err}`);
    }).on('progress', function(progress, data) {
      console.log(`Notification job ${jobQueue.id} ${progress}% complete`)
    });
  });
}