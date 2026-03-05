#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {authenticate} from '@google-cloud/local-auth';
import {google} from 'googleapis';

const SCOPES = ['https://www.googleapis.com/auth/calendar'];
const BASE = path.resolve(process.cwd(), 'tools/calendar');
const TOKEN_PATH = path.join(BASE, 'token.json');
const CREDENTIALS_PATH = path.join(BASE, 'credentials.json');

async function loadSavedCredentialsIfExist() {
  if (!fs.existsSync(TOKEN_PATH)) return null;
  const content = fs.readFileSync(TOKEN_PATH, 'utf8');
  const credentials = JSON.parse(content);
  return google.auth.fromJSON(credentials);
}

function saveCredentials(client) {
  const keys = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
  const key = keys.installed || keys.web;
  const payload = JSON.stringify({
    type: 'authorized_user',
    client_id: key.client_id,
    client_secret: key.client_secret,
    refresh_token: client.credentials.refresh_token,
  });
  fs.writeFileSync(TOKEN_PATH, payload);
}

async function authorize() {
  let client = await loadSavedCredentialsIfExist();
  if (!client) {
    if (!fs.existsSync(CREDENTIALS_PATH)) {
      throw new Error(`Missing OAuth credentials: ${CREDENTIALS_PATH}`);
    }
    client = await authenticate({
      scopes: SCOPES,
      keyfilePath: CREDENTIALS_PATH,
    });
    if (client.credentials) saveCredentials(client);
  }
  return client;
}

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : fallback;
}

async function main() {
  const cmd = process.argv[2];
  const auth = await authorize();
  const calendar = google.calendar({version: 'v3', auth});
  const calendarId = arg('calendar', 'primary');

  if (cmd === 'create') {
    const title = arg('title');
    const description = arg('description', '');
    const timezone = arg('timezone', 'Australia/Adelaide');
    const allDay = process.argv.includes('--all-day');
    const body = {summary: title, description};
    if (allDay) {
      body.start = {date: arg('start-date')};
      body.end = {date: arg('end-date')};
    } else {
      body.start = {dateTime: arg('start'), timeZone: timezone};
      body.end = {dateTime: arg('end'), timeZone: timezone};
    }
    const res = await calendar.events.insert({calendarId, requestBody: body});
    console.log(JSON.stringify({id: res.data.id, htmlLink: res.data.htmlLink}));
    return;
  }

  if (cmd === 'update') {
    const eventId = arg('event-id');
    const timezone = arg('timezone', 'Australia/Adelaide');
    const getRes = await calendar.events.get({calendarId, eventId});
    const event = getRes.data;
    const title = arg('title');
    if (title) event.summary = title;
    const description = arg('description');
    if (description !== null) event.description = description;
    const start = arg('start');
    const end = arg('end');
    if (start && end) {
      event.start = {dateTime: start, timeZone: timezone};
      event.end = {dateTime: end, timeZone: timezone};
    }
    const res = await calendar.events.update({calendarId, eventId, requestBody: event});
    console.log(JSON.stringify({id: res.data.id, htmlLink: res.data.htmlLink}));
    return;
  }

  if (cmd === 'list') {
    const timeMin = arg('time-min');
    const timeMax = arg('time-max');
    const maxResults = Number(arg('limit', '20'));
    const res = await calendar.events.list({
      calendarId,
      timeMin,
      timeMax,
      singleEvents: true,
      orderBy: 'startTime',
      maxResults,
    });
    for (const e of res.data.items || []) {
      const start = e.start?.dateTime || e.start?.date;
      console.log(`${e.id}\t${start}\t${e.summary || '(no title)'}`);
    }
    return;
  }

  throw new Error('Usage: gcal_quick.mjs <create|update|list> ...');
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
