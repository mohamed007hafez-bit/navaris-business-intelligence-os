#!/usr/bin/env node
'use strict';
/** NAVARIS outreach preparation only. No email sending, vendor contact, or bid submission. */
const fs=require('node:fs'),path=require('node:path');
const input=path.resolve(process.argv[2]||path.join(__dirname,'..','docs','suppliers-qualified.json'));
const output=path.resolve(process.argv[3]||path.join(__dirname,'..','docs','outreach-drafts.json'));
const keys=['identity','track_record','capacity','eligibility','terms'];
const opportunities=[
{id:'SPE605-26-R-0218',name:'DLA Energy Guam fuel solicitation',url:'https://sam.gov/opp/87ea94da26dc4b8ab4558da8b484e841/view',status:'VERIFY_CURRENT_NOTICE'},
{id:'SPE608-26-R-0206',name:'DLA Energy Progreso JP-5 transportation',url:'https://sam.gov/opp/a24fe5a4ec26476385b67865f51500e0/view',status:'VERIFY_CURRENT_NOTICE'},
{id:'CO-LOADING',name:'Co-loading / logistics coordination',url:'',status:'REQUIRES_COUNTERPARTY_SPECIFIC_DETAILS'}];
const additionalLeads=[
{name:'Senghor-associated lead',status:'UNVERIFIED_LEAD',note:'Verify exact legal entity, contact, authority, capability and compliance.'},
{name:'AAMRO-associated lead',status:'UNVERIFIED_LEAD',note:'Verify exact legal entity, contact, authority, capability and compliance.'},
{name:'MGL-associated lead',status:'UNVERIFIED_LEAD',note:'Verify exact legal entity, contact, authority, capability and compliance.'}];
function fail(m){console.error(m);process.exit(1)}
if(!fs.existsSync(input))fail('Supplier JSON not found: '+input);
let data;try{data=JSON.parse(fs.readFileSync(input,'utf8'))}catch(e){fail('Invalid JSON: '+e.message)}
if(!Array.isArray(data.suppliers))fail('Expected suppliers array');
const drafts=[];
for(const s of data.suppliers){if(!keys.every(k=>s.gates?.[k]===true)||!s.name||!s.contact)continue;
for(const o of opportunities)drafts.push({recipient:s.contact,subject:'NAVARIS | Preliminary partner-fit inquiry — '+o.name,opportunity:o,supplier:s.name,draftOnly:true,status:'DRAFT_NOT_SENT',body:'Hello,\n\nNAVARIS Business Operations & Development is screening counterparties for a potential '+o.name+' opportunity. This is a preliminary capability inquiry only; it is not a representation that any party is eligible.\n\nPlease confirm your exact legal entity, official registration identifiers, relevant performance references, capacity for the stated scope/route, permits and eligibility under the current solicitation. Please also confirm whether your compliance team permits a lawful written referral/commission arrangement. Any NCNDA and fee agreement must be reviewed and signed before introductions. NAVARIS will not finance procurement, transport, inventory, guarantees or advances.\n\nPlease share official evidence and the appropriate compliance/business contact. No bid or external commitment is made by this message.\n\nRegards,\nNAVARIS | Business Operations & Development'});}
const result={generated_at:new Date().toISOString(),mode:'DRAFT_ONLY_NO_SEND',source:input,qualification_rule:'all five gates must be true',opportunities,additionalLeads,drafts,summary:{supplier_count:data.suppliers.length,fully_gated_suppliers:data.suppliers.filter(s=>keys.every(k=>s.gates?.[k]===true)).length,drafts_generated:drafts.length}};
fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n','utf8');console.log(JSON.stringify({output,mode:result.mode,...result.summary},null,2));
