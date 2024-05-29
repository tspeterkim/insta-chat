// Shows the sidebar
function showSidebar() {
    const htmlOutput = HtmlService.createHtmlOutputFromFile('Sidebar').setTitle('Insta Posts');
    SpreadsheetApp.getUi().showSidebar(htmlOutput);
}

// Stores the tokens that bot.py will use to send auto-replies
function storeToken(accessToken, page_id) {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    sheet.getRange('Z1').setValue(accessToken);
    sheet.getRange('Z2').setValue(page_id)
}