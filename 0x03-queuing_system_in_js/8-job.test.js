import { describe, it, before, after, afterEach } from 'mocha';
import { expect } from 'chai';
import { createQueue } from 'kue';
import sinon from 'sinon';
import creacreatePushNotificationsJobs from './8-job';

const queue = createQueue();

describe('createPushNotificationsJobs test', () => {
  before(() => {
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => creacreatePushNotificationsJobs('test not array', queue)).to.throw(Error, 'Jobs is not an array');
  });

  it('should create jobs in the queue when given valid array', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      },
    ];

    creacreatePushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
  });

  it('should not create any jobs if the jobs array is empty', () => {
    creacreatePushNotificationsJobs([], queue);
    expect(queue.testMode.jobs.length).to.equal(0);
  });
});