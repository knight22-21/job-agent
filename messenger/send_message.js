import { makeWASocket, useMultiFileAuthState, fetchLatestBaileysVersion } from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import fs from 'fs';
import path from 'path';

// Load group IDs from messages.json (adjust path if needed)
const groupData = JSON.parse(fs.readFileSync('./messages.json', 'utf-8'));

// Load job data from data/jobs_filtered.json
const jobsFilePath = path.join('data', 'jobs_filtered.json');
const jobListings = JSON.parse(fs.readFileSync(jobsFilePath, 'utf-8'));

async function startBot() {
  const { state, saveCreds } = await useMultiFileAuthState('auth_info');
  const { version } = await fetchLatestBaileysVersion();
  const sock = makeWASocket({
    version,
    auth: state,
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', (update) => {
    if (update.qr) {
      console.log('Scan this QR code:');
      qrcode.generate(update.qr, { small: true });
    }
    if (update.connection === 'close') {
      console.log('Connection closed, reconnecting...');
      startBot();
    } else if (update.connection === 'open') {
      console.log('Connected to WhatsApp!');
      sendMessages();
    }
  });

  async function sendMessages() {
    if (!Array.isArray(jobListings) || jobListings.length === 0) {
      console.error('No job listings found.');
      return;
    }

    // Format job listings
    const formattedJobs = jobListings.map(job => {
      return `📌 *${job.title}*\n🏢 Company: ${job.company}\n🌍 Location: ${job.location}\n🔗 Apply: ${job.url}`;
    }).join('\n\n');

    for (const { groupId } of groupData) {
      if (!groupId) {
        console.warn('Skipping invalid group ID.');
        continue;
      }

      try {
        // Send message using groupId internally, but don't print it
        await sock.sendMessage(groupId, { text: formattedJobs });
      } catch (e) {
        console.error('Failed to send message to a group.');
      }
    }

    setTimeout(() => {
      console.log("All messages sent. Exiting...");
      process.exit(0);
    }, 2000);
  }
}

startBot();
