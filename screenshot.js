const screenshot = require('screenshot-desktop');

screenshot().then((img) => {
  const fs = require('fs');
  fs.writeFileSync('/Users/konglingzheng/.openclaw/workspace/screenshot.png', img);
  console.log('Screenshot saved to /Users/konglingzheng/.openclaw/workspace/screenshot.png');
}).catch(err => {
  console.error('Error taking screenshot:', err);
  process.exit(1);
});
