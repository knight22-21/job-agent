import { makeWASocket, useMultiFileAuthState, fetchLatestBaileysVersion } from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import { exec } from 'child_process';
import fs from 'fs';

async function startListener() {
  const { state, saveCreds } = await useMultiFileAuthState('auth_info_listener');
  const { version } = await fetchLatestBaileysVersion();

  // Load group data from JSON file
  const groupData = JSON.parse(fs.readFileSync('./messages.json', 'utf-8'));
  console.log('Authorized group access configured');

  const sock = makeWASocket({
    version,
    auth: state,
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', (update) => {
    if (update.qr) {
      console.log('Scan the QR code to log in:');
      qrcode.generate(update.qr, { small: true });
    }

    if (update.connection === 'close') {
      console.log('Connection lost. Attempting to reconnect...');
      startListener();
    } else if (update.connection === 'open') {
      console.log('Bot is connected and ready');
    }
  });

  sock.ev.on('messages.upsert', async ({ messages }) => {
    const msg = messages[0];
    if (!msg.message) {
      console.log("Empty message received. Ignored.");
      return;
    }
    if (msg.key.fromMe) {
      console.log("Own message detected. Ignored.");
      return;
    }

    const body = msg.message.conversation || msg.message.extendedTextMessage?.text || '';
    const jid = msg.key.remoteJid;

    if (body.trim() !== "!jobbot") {
      console.log('Non-command message received. Ignored.');
      return;
    }

    const authorizedGroup = groupData.find(group => group.groupId === jid);
    if (!authorizedGroup) {
      console.log('Command received from an unauthorized group.');
      await sock.sendMessage(jid, { text: "This group is not allowed to run the job agent." });
      return;
    }

    try {
      const metadata = await sock.groupMetadata(jid);
      const sender = msg.key.participant || msg.key.remoteJid;

      const participant = metadata.participants.find(p => p.id === sender);
      const isAdmin = participant?.admin === 'admin' || participant?.admin === 'superadmin';

      if (!isAdmin) {
        console.log('Unauthorized user attempted to run the job agent.');
        await sock.sendMessage(jid, { text: "You are not allowed to run the job agent." });
        return;
      }

      console.log('Authorized command received. Running job agent...');
      exec("python main.py run", async (error, stdout, stderr) => {
        if (error) {
          console.log('Job agent failed to execute.');
          await sock.sendMessage(jid, { text: "Failed to run the job agent." });
        } else {
          console.log('Job agent execution completed.');
          await sock.sendMessage(jid, { text: "Job agent completed successfully." });
        }
      });
    } catch (err) {
      console.log("An error occurred while processing the command.");
      await sock.sendMessage(jid, { text: "Something went wrong while handling the command." });
    }
  });
}

startListener();
