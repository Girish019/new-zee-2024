
# A simple format under pic
FOMET = """
Ꮛᴘɪᴤοᴅє ŋο   ➺  <b>[{}] {}</b>

▬▬▬▬▬ ✮✯☆★ ❂ ★☆✯✮ ▬▬▬▬▬
       
𝕯𝖆𝖙𝖊 ➻ <b>{}</b>

             𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐛𝐲  ➠  @Dot_serials_bot 

                       ⚜⚜⚜⍟⚜⚜⚜    
 
    YOUR EPISODE LINK 🔗 
<b>{}</b>
<b>{}</b>

        👀👩‍💻 𝐇𝐨𝐰 𝐭𝐨 𝐨𝐩𝐞𝐧 👩‍💻👀
https://t.me/+Sb5ro1gyhgY0NWM1
https://t.me/+Sb5ro1gyhgY0NWM1
  """
# A simple format return sent elements datails see (line 72, 39 in pluggins->channel post)
BOTEFITMSG = """
Post Sent Successfully ✅
Elements in <b>"{}"</b>

<b>TG Link : <a href="{}">Tlink</a></b> & <b>Short Link: <a href="{}">SLink</a></b>
<b>Vid Size : {}</b>   <b>Date : {}</b>
"""
#whole serials data return in dictionary
############{'serial name':["pic", "short link domin", "short link api", "To channel id"]}###############
#ex =>>>    '':['','','','']
DATAODD = {
        'Trinayani':['https://graph.org/file/1f2827a0980cc418ee6e1.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001942664190'],
        'Annapoorna':['https://graph.org/file/baff21a920cc09f0ba89a.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001942664190'],
        'Kalyanamasthu':['https://graph.org/file/db7a3d7d1a2654540cf99.jpg','upshrink.com','7864f20bc9c1eb4c29769f820c1069ddd21dfe94','-1001942664190'],
        'Vaidehi_Parinaya':['https://graph.org/file/8c7eda434e1f0baae0b81.jpg','upshrink.com','7864f20bc9c1eb4c29769f820c1069ddd21dfe94','-1001942664190'],
        'Punarvivaha':['https://graph.org/file/70d5850fd6e9ed8cd7bc0.jpg','upshrink.com','4a6aae0ff4e202d6c04695352f6409511f2a0642','-1001942664190'],
        'Paaru':['https://graph.org/file/f4eccb711889b4e33952a.jpg','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001942664190'],
        'Bhoomige_Bandha_Bhagavantha':['https://graph.org/file/dc3b179fceb487e4847c4.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001942664190'],
        'Puttakkana_Makkalu':['https://graph.org/file/085afbc67400a2066fefd.jpg','tnshort.net','cfafc72b0df2558f0f5ad4e1c906ce9f783281e3','-1001942664190'],
        'Gattimela':['https://graph.org/file/d3eda0e1961ee06e5cba7.jpg','linkshortify.com','9e82f5e0d917c633234194f39c2985752efd67e0','-1001942664190'],
        'Manemagalu':['https://graph.org/file/979b1125f1b333d1b8b07.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001942664190'],
        'Sandhyaraaga':['https://graph.org/file/98ef89a04dd66bef924ea.jpg','upshrink.com','4a6aae0ff4e202d6c04695352f6409511f2a0642','-1001942664190'],
        'SeethaRaama':['https://graph.org/file/d7b3c98a89d0d061f064f.jpg','tnshort.net','0045de7eda3a082a38f05bdd0d1c4de1262709fb','-1001942664190'],
        'Amruthadhaare':['https://graph.org/file/2ebe4f1d999849a1ca574.jpg','linkshortify.com','8a9a3df5db074b2b1ad10efcd383e5243118447b','-1001942664190'],
        'Mahanayaka_Dr_B_R_Ambedkar':['https://graph.org/file/6faf520d534a49f6742bb.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001942664190'],
        'Shrirasthu':['https://graph.org/file/b6d93c7cc15166fbf7e35.jpg','moneycase.link','f35b0c3ac535a200b3287c698b652e58b4689b6f','-1001942664190'],
        'Soubhagyavati_Bhava':['https://graph.org/file/2d34fb7705e6ecb7c5937.jpg','tnvalue.in','8fc4e5a5a7f1d571adfc7c02537d7c1e73da1a15','-1001942664190'],
        'Hitler_Kalyana':['https://graph.org/file/4bccb3c8fd1fe4c5d92e7.jpg','linkshortify.com','4bc6f1e34d0409e5b8bd2197d42462bb1ec6048a','-1001942664190'],
        'Sathya':['https://graph.org/file/7f30ff54ecf9b380e4634.jpg','tnshort.net','1183b34c88b1fd4e898d7d9dc7b6fc6a2bea9dd9','-1001942664190'],
        'Dance_Karnataka_Dance_Season_7':['https://graph.org/file/2d724f7a19f736c405990.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001942664190'],
        'Bharjari_Bachelors':['https://graph.org/file/1b28fb7863cc31f732ac4.jpg','tnvalue.in','8fc4e5a5a7f1d571adfc7c02537d7c1e73da1a15','-1001942664190'],
        'Couples_Kitchen':['https://graph.org/file/07d7a9c7707eac7367842.jpg','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001942664190'],
        "Couple's_Kitchen_":['https://graph.org/file/07d7a9c7707eac7367842.jpg','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001942664190'],
        'Chota_Champion':['https://graph.org/file/0d77fc85da98174336f8b.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001942664190'],
        'Jodi_No_1_Season_2':['https://graph.org/file/034b0251e3e3cbc172ddf.jpg','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001942664190'],
        'Sa_Re_Ga_Ma_Pa_Season_20':['https://graph.org/file/7ef74d66ba659081feab3.jpg','tnvalue.in','8fc4e5a5a7f1d571adfc7c02537d7c1e73da1a15','-1001942664190'],
        'Drama_Juniors_Season_5':['https://graph.org/file/d8b1e16b46a0c6a4850fe.jpg','moneycase.link','f35b0c3ac535a200b3287c698b652e58b4689b6f','-1001942664190'],
  
        'Pavada_Purasha':['https://graph.org/file/f65651907ba441187f7b1.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001965277713'],
        'Olavina_Nildana':['https://graph.org/file/441e02c5e145609e0eedd.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001965277713'],
        'Kendasampige':['https://graph.org/file/62c90177d09f7cf416e6c.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001965277713'],
        'Bhagyalakshmi':['https://graph.org/file/261d0c995b5e2a434093b.jpg','linkshortify.com','4bc6f1e34d0409e5b8bd2197d42462bb1ec6048a','-1001965277713'],
        'Ramachari':['https://graph.org/file/f590c3585b4c0068df630.jpg','tnshort.net','0045de7eda3a082a38f05bdd0d1c4de1262709fb','-1001965277713'],
        'Lakshmi_Baramma':['https://graph.org/file/be3588e70978523792514.jpg','linkshortify.com','9e82f5e0d917c633234194f39c2985752efd67e0','-1001965277713'],
        'Geetha':['https://graph.org/file/e95baeeafbf180bd184e1.jpg','tnshort.net','cfafc72b0df2558f0f5ad4e1c906ce9f783281e3','-1001965277713'],
        'Lakshana':['https://graph.org/file/995a7a33f5d543f4f4dbf.jpg','linkshortify.com','8a9a3df5db074b2b1ad10efcd383e5243118447b','-1001965277713'],
        'Punyavathi':['https://graph.org/file/c15998a362846c9eb09f0.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001965277713'],
        'Tripura_Sundari':['https://graph.org/file/4a59fd893093b82e9c234.jpg','tnvalue.in','8fc4e5a5a7f1d571adfc7c02537d7c1e73da1a15','-1001965277713'],
        'Antarapata':['https://graph.org/file/ea08c222d4848f1661e3c.jpg','tnshort.net','1183b34c88b1fd4e898d7d9dc7b6fc6a2bea9dd9','-1001965277713'],
        'Gruhapravesha':['https://graph.org/file/16220456e337fa35b18b7.jpg','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001965277713'],
        'Ganda_Hendthi':['https://graph.org/file/e7437d0a9eac55fdb2623.jpg','moneycase.link','f35b0c3ac535a200b3287c698b652e58b4689b6f','-1001965277713'],
        'Shantham_Papam':['https://graph.org/file/fa897d25d4d944e8487d5.jpg','upshrink.com','4a6aae0ff4e202d6c04695352f6409511f2a0642','-1001965277713'],
        'Muddu_Bangara':['https://graph.org/file/49001901d7ccbf8698935.jpg','upshrink.com','7864f20bc9c1eb4c29769f820c1069ddd21dfe94','-1001965277713'],
        'Gunasundari':['https://graph.org/file/8d4b6b2e9703a7d97b546.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001965277713'],
        'Anu':['https://graph.org/file/7a8f5ce25159932859193.jpg','onepagelink.in','5b9b84dfbc7b58a84ae25a75e2b5cf4fec69a4eb','-1001965277713'],
        'Family_Gangstars':['https://graph.org/file/d08c55a1b259a3b5c95b7.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001965277713'],
        'Brundavana':['https://te.legra.ph/file/400cc7b9a9dcc1c1d230e.jpg','linkshortify.com','9e82f5e0d917c633234194f39c2985752efd67e0','-1001965277713'],
        'Shiva_Shakthi':['https://te.legra.ph/file/cd50cd7409c99d938aace.jpg','Upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001965277713'],
        'Bigg_Boss_Kannada':['https://graph.org/file/011900e64399568f3fe93.jpg','linkshortify.com','4bc6f1e34d0409e5b8bd2197d42462bb1ec6048a','-1001335177183'],
  
        'Neenadhe_Naa':['https://graph.org/file/fcbbf0a8c0413d4a59ad9.jpg','tnshort.net','0045de7eda3a082a38f05bdd0d1c4de1262709fb','-1001901182731'],
        'Namma_Lachi':['https://graph.org/file/b315e59c10e04d1b2e595.jpg','linkshortify.com','4bc6f1e34d0409e5b8bd2197d42462bb1ec6048a','-1001901182731'],
        'Nagapanchami':['https://graph.org/file/dd2a58d339ca517010edc.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001901182731'],
        'Raani':['https://graph.org/file/5a8aed0bcd6e14604b5d8.jpg','tnshort.net','cfafc72b0df2558f0f5ad4e1c906ce9f783281e3','-1001901182731'],
        'Katheyondu_Shuruvagide':['https://img1.hotstarext.com/image/upload/sources/r1/cms/prod/1003/1491003-h-1d7e2dcf91ca','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001901182731'],
        'O_MuddhuManase':['https://graph.org/file/cd2664a143bec7e2d5f14.jpg','tnshort.net','1183b34c88b1fd4e898d7d9dc7b6fc6a2bea9dd9','-1001901182731'],
        'Jenugudu':['https://graph.org/file/48a8df66387287f6e2440.jpg','linkshortify.com','9e82f5e0d917c633234194f39c2985752efd67e0','-1001901182731'],
        'Udho_Udho_Shri_Renuka_Yellamma':['https://graph.org/file/f5749c1343173f855b0e7.jpg','upshrink.com','7864f20bc9c1eb4c29769f820c1069ddd21dfe94','-1001901182731'],
        'Aragini_2':['https://graph.org/file/6ddd25521aa2c813306aa.jpg','moneycase.link','f35b0c3ac535a200b3287c698b652e58b4689b6f','-1001901182731'],
        'Honganasu':['https://graph.org/file/ca9bcfcfb5560459c3bcf.jpg','tnvalue.in','8fc4e5a5a7f1d571adfc7c02537d7c1e73da1a15','-1001901182731'],
        'Anuraga_Aralitu':['https://graph.org/file/0b15dd8c7f1d0118af62e.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001901182731'],
        'Anupama_Sarvagunaa_Sampanne':['https://graph.org/file/0e86ebb3ab5cf24eac6c9.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001901182731'],
        'Yediyur_Shree_Siddhalingeshwara':['https://graph.org/file/20ff06892579f4e3ac9ed.jpg','upshrink.com','4a6aae0ff4e202d6c04695352f6409511f2a0642','-1001901182731'],
        'Bombat_Bhojana':['https://graph.org/file/d2871411e7358e4c76b52.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001901182731'],
        'Suvarna_Superstar':['https://graph.org/file/09f90f559d100a415f393.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001901182731'],
        'Kaveri_Kannada_Medium':['https://graph.org/file/b53472a77d733b99b2f05.jpg','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001901182731'],
        'Avanu_Matthe_Shravani':['https://graph.org/file/c0403382ffa200212ae4f.jpg','tnshort.net','1183b34c88b1fd4e898d7d9dc7b6fc6a2bea9dd9','-1001901182731'],
        'Kaveri_Kannada_Medium':['https://graph.org/file/ba76be791996ad8f45928.jpg','tnshort.net','cfafc72b0df2558f0f5ad4e1c906ce9f783281e3','-1001901182731'],
        'Gowri_Shankara':['https://graph.org/file/074cc5c27be51345717eb.jpg','linkshortify.com','8a9a3df5db074b2b1ad10efcd383e5243118447b','-1001901182731'],
        'Aase':['https://te.legra.ph/file/2e41e0ab4cf35e473de3c.jpg','Upshrink.com','7864f20bc9c1eb4c29769f820c1069ddd21dfe94','-1001901182731'],
        'Gowri_Shankara':['https://te.legra.ph/file/eb2395587b3562a729c68.jpg','Upshrink.com','4a6aae0ff4e202d6c04695352f6409511f2a0642','-1001901182731']
}
DATAEVEN = {
        'Trinayani':['https://graph.org/file/1f2827a0980cc418ee6e1.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001942664190'],
        'Annapoorna':['https://graph.org/file/baff21a920cc09f0ba89a.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001942664190'],
        'Kalyanamasthu':['https://graph.org/file/db7a3d7d1a2654540cf99.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001942664190'],
        'Vaidehi_Parinaya':['https://graph.org/file/8c7eda434e1f0baae0b81.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001942664190'],
        'Punarvivaha':['https://graph.org/file/70d5850fd6e9ed8cd7bc0.jpg','upshrink.com','7864f20bc9c1eb4c29769f820c1069ddd21dfe94','-1001942664190'],
        'Paaru':['https://graph.org/file/f4eccb711889b4e33952a.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001942664190'],
        'Bhoomige_Bandha_Bhagavantha':['https://graph.org/file/dc3b179fceb487e4847c4.jpg','tnvalue.in','8fc4e5a5a7f1d571adfc7c02537d7c1e73da1a15','-1001942664190'],
        'Puttakkana_Makkalu':['https://graph.org/file/085afbc67400a2066fefd.jpg','linkshortify.com','9e82f5e0d917c633234194f39c2985752efd67e0','-1001942664190'],
        'Gattimela':['https://graph.org/file/d3eda0e1961ee06e5cba7.jpg','tnshort.net','cfafc72b0df2558f0f5ad4e1c906ce9f783281e3','-1001942664190'],
        'Manemagalu':['https://graph.org/file/979b1125f1b333d1b8b07.jpg','upshrink.com','4a6aae0ff4e202d6c04695352f6409511f2a0642','-1001942664190'],
        'Sandhyaraaga':['https://graph.org/file/98ef89a04dd66bef924ea.jpg','upshrink.com','7864f20bc9c1eb4c29769f820c1069ddd21dfe94','-1001942664190'],
        'SeethaRaama':['https://graph.org/file/d7b3c98a89d0d061f064f.jpg','linkshortify.com','4bc6f1e34d0409e5b8bd2197d42462bb1ec6048a','-1001942664190'],
        'Amruthadhaare':['https://graph.org/file/2ebe4f1d999849a1ca574.jpg','tnshort.net','1183b34c88b1fd4e898d7d9dc7b6fc6a2bea9dd9','-1001942664190'],
        'Mahanayaka_Dr_B_R_Ambedkar':['https://graph.org/file/6faf520d534a49f6742bb.jpg','tnvalue.in','8fc4e5a5a7f1d571adfc7c02537d7c1e73da1a15','-1001942664190'],
        'Shrirasthu_Shubhamasthu':['https://graph.org/file/b6d93c7cc15166fbf7e35.jpg','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001942664190'],
        'Soubhagyavati_Bhava':['https://graph.org/file/2d34fb7705e6ecb7c5937.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001942664190'],
        'Hitler_Kalyana':['https://graph.org/file/4bccb3c8fd1fe4c5d92e7.jpg','tnshort.net','0045de7eda3a082a38f05bdd0d1c4de1262709fb','-1001942664190'],
        'Sathya':['https://graph.org/file/7f30ff54ecf9b380e4634.jpg','linkshortify.com','8a9a3df5db074b2b1ad10efcd383e5243118447b','-1001942664190'],
        'Dance_Karnataka_Dance_Season_7':['https://graph.org/file/2d724f7a19f736c405990.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001942664190'],
        'Bharjari_Bachelors':['https://graph.org/file/1b28fb7863cc31f732ac4.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001942664190'],
        'Couples_Kitchen':['https://graph.org/file/07d7a9c7707eac7367842.jpg','moneycase.link','f35b0c3ac535a200b3287c698b652e58b4689b6f','-1001942664190'],
        "Couple's_Kitchen_":['https://graph.org/file/07d7a9c7707eac7367842.jpg','moneycase.link','f35b0c3ac535a200b3287c698b652e58b4689b6f','-1001942664190'],
        'Chota_Champion':['https://graph.org/file/0d77fc85da98174336f8b.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001942664190'],
        'Jodi_No_1_Season_2':['https://graph.org/file/034b0251e3e3cbc172ddf.jpg','moneycase.link','f35b0c3ac535a200b3287c698b652e58b4689b6f','-1001942664190'],
        'Sa_Re_Ga_Ma_Pa_Season_20':['https://graph.org/file/7ef74d66ba659081feab3.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001942664190'],
        'Drama_Juniors_Season_5':['https://graph.org/file/d8b1e16b46a0c6a4850fe.jpg','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001942664190'],
  
        'Pavada_Purasha':['https://graph.org/file/f65651907ba441187f7b1.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001965277713'],
        'Olavina_Nildana':['https://graph.org/file/441e02c5e145609e0eedd.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001965277713'],
        'Kendasampige':['https://graph.org/file/62c90177d09f7cf416e6c.jpg','upshrink.com','4a6aae0ff4e202d6c04695352f6409511f2a0642','-1001965277713'],
        'Bhagyalakshmi':['https://graph.org/file/261d0c995b5e2a434093b.jpg','tnshort.net','0045de7eda3a082a38f05bdd0d1c4de1262709fb','-1001965277713'],
        'Ramachari':['https://graph.org/file/f590c3585b4c0068df630.jpg','linkshortify.com','4bc6f1e34d0409e5b8bd2197d42462bb1ec6048a','-1001965277713'],
        'Lakshmi_Baramma':['https://graph.org/file/be3588e70978523792514.jpg','tnshort.net','cfafc72b0df2558f0f5ad4e1c906ce9f783281e3','-1001965277713'],
        'Geetha':['https://graph.org/file/e95baeeafbf180bd184e1.jpg','linkshortify.com','9e82f5e0d917c633234194f39c2985752efd67e0','-1001965277713'],
        'Lakshana':['https://graph.org/file/995a7a33f5d543f4f4dbf.jpg','tnshort.net','1183b34c88b1fd4e898d7d9dc7b6fc6a2bea9dd9','-1001965277713'],
        'Punyavathi':['https://graph.org/file/c15998a362846c9eb09f0.jpg','tnvalue.in','8fc4e5a5a7f1d571adfc7c02537d7c1e73da1a15','-1001965277713'],
        'Tripura_Sundari':['https://graph.org/file/4a59fd893093b82e9c234.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001965277713'],
        'Antarapata':['https://graph.org/file/ea08c222d4848f1661e3c.jpg','linkshortify.com','8a9a3df5db074b2b1ad10efcd383e5243118447b','-1001965277713'],
        'Gruhapravesha':['https://graph.org/file/16220456e337fa35b18b7.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001965277713'],
        'Ganda_Hendthi':['https://graph.org/file/e7437d0a9eac55fdb2623.jpg','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001965277713'],
        'Shantham_Papam':['https://graph.org/file/fa897d25d4d944e8487d5.jpg','upshrink.com','7864f20bc9c1eb4c29769f820c1069ddd21dfe94','-1001965277713'],
        'Muddu_Bangara':['https://graph.org/file/49001901d7ccbf8698935.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001965277713'],
        'Gunasundari':['https://graph.org/file/8d4b6b2e9703a7d97b546.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001965277713'],
        'Anu':['https://graph.org/file/7a8f5ce25159932859193.jpg','upshrink.com','2853363dbc172344dd8b979c9ff097d2a0ff4714','-1001965277713'],
        'Family_Gangstars':['https://graph.org/file/d08c55a1b259a3b5c95b7.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001965277713'],
        'Brundavana':['https://te.legra.ph/file/400cc7b9a9dcc1c1d230e.jpg','linkshortify.com','9e82f5e0d917c633234194f39c2985752efd67e0','-1001965277713'],
        'Shiva_Shakthi':['https://te.legra.ph/file/cd50cd7409c99d938aace.jpg','Upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001965277713'],
        'Bigg_Boss_Kannada':['https://graph.org/file/011900e64399568f3fe93.jpg','tnshort.net','0045de7eda3a082a38f05bdd0d1c4de1262709fb','-1001335177183'],

        'Neenadhe_Naa':['https://graph.org/file/fcbbf0a8c0413d4a59ad9.jpg','linkshortify.com','4bc6f1e34d0409e5b8bd2197d42462bb1ec6048a','-1001901182731'],
        'Namma_Lachi':['https://graph.org/file/b315e59c10e04d1b2e595.jpg','tnshort.net','0045de7eda3a082a38f05bdd0d1c4de1262709fb','-1001901182731'],
        'Nagapanchami':['https://graph.org/file/dd2a58d339ca517010edc.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001901182731'],
        'Raani':['https://graph.org/file/5a8aed0bcd6e14604b5d8.jpg','linkshortify.com','9e82f5e0d917c633234194f39c2985752efd67e0','-1001901182731'],
        'Katheyondu_Shuruvagide':['https://img1.hotstarext.com/image/upload/sources/r1/cms/prod/1003/1491003-h-1d7e2dcf91ca','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001901182731'],
        'O_MuddhuManase':['https://graph.org/file/cd2664a143bec7e2d5f14.jpg','linkshortify.com','8a9a3df5db074b2b1ad10efcd383e5243118447b','-1001901182731'],
        'Jenugudu':['https://graph.org/file/48a8df66387287f6e2440.jpg','tnshort.net','cfafc72b0df2558f0f5ad4e1c906ce9f783281e3','-1001901182731'],
        'Udho_Udho_Shri_Renuka_Yellamma':['https://graph.org/file/f5749c1343173f855b0e7.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001901182731'],
        'Aragini_2':['https://graph.org/file/6ddd25521aa2c813306aa.jpg','tnvalue.in','e496ab76b42f51628da20bb69577397533008f3c','-1001901182731'],
        'Honganasu':['https://graph.org/file/ca9bcfcfb5560459c3bcf.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001901182731'],
        'Anuraga_Aralitu':['https://graph.org/file/0b15dd8c7f1d0118af62e.jpg','upshrink.com','db8e518b1e15d2184e0dfe7467a6e6e92f4ccbf4','-1001901182731'],
        'Anupama_Sarvagunaa_Sampanne':['https://graph.org/file/0e86ebb3ab5cf24eac6c9.jpg','tnvalue.in','8fc4e5a5a7f1d571adfc7c02537d7c1e73da1a15','-1001901182731'],
        'Yediyur_Shree_Siddhalingeshwara':['https://graph.org/file/20ff06892579f4e3ac9ed.jpg','upshrink.com','7864f20bc9c1eb4c29769f820c1069ddd21dfe94','-1001901182731'],
        'Bombat_Bhojana':['https://graph.org/file/d2871411e7358e4c76b52.jpg','upshrink.com','4a6aae0ff4e202d6c04695352f6409511f2a0642','-1001901182731'],
        'Suvarna_Superstar':['https://graph.org/file/09f90f559d100a415f393.jpg','tnvalue.in','ff426552eda72230153ea3450a0bce0557183ccb','-1001901182731'],
        'Kaveri_Kannada_Medium':['https://graph.org/file/b53472a77d733b99b2f05.jpg','moneycase.link','bdc62bf7dd54515abf15371b58feb6a1ff2b434a','-1001901182731'],
        'Avanu_Matthe_Shravani':['https://graph.org/file/c0403382ffa200212ae4f.jpg','linkshortify.com','4bc6f1e34d0409e5b8bd2197d42462bb1ec6048a','-1001901182731'],
        'Kaveri_Kannada_Medium':['https://graph.org/file/ba76be791996ad8f45928.jpg','linkshortify.com','9e82f5e0d917c633234194f39c2985752efd67e0','-1001901182731'],
        'Gowri_Shankara':['https://graph.org/file/074cc5c27be51345717eb.jpg','tnshort.net','1183b34c88b1fd4e898d7d9dc7b6fc6a2bea9dd9','-1001901182731'],
        'Aase':['https://te.legra.ph/file/2e41e0ab4cf35e473de3c.jpg','Upshrink.com','4a6aae0ff4e202d6c04695352f6409511f2a0642','-1001901182731'],
        'Gowri_Shankara':['https://te.legra.ph/file/eb2395587b3562a729c68.jpg','Upshrink.com','7864f20bc9c1eb4c29769f820c1069ddd21dfe94','-1001901182731']
}

