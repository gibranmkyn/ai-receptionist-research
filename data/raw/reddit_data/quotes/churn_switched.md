# Verbatim Quotes — Churn Switched

**Source:** Reddit (via Arctic Shift)  
**Collected:** 2026-02-11  
**Status:** Collecting (updates live)

---

### r/LawFirm — 2025-02-11 | 3pts

> I have absolutely no doubt that there are better or cheaper options than Ring Central, but I have no reason to seek them out.  Back in the ice age when I first opened an office, I had four phone lines - one main line, two "back office" lines and a dedicated fax line.  I paid AT&T something like $450/month for all that shit, and had a phone system with eight handsets in the office that I leased for some crazy amount - like $200/month.

Fast forward ten years, and I got rid of the two "back office" lines and the leased phone system.  So then I was only paying AT&T $250/month.  

Fast forward another five years, and I switched phone companies to a small service that ported my main number to a remote receptionist and my fax number to an efax service.  The phone bill went down to maybe $100/month.

Finally, I ditched everything and pay RingCentral maybe $50/month.  I can make phone calls from my "main line" on any device.  I can send and receive text messages.  I can send and receive faxes.  The app isn't great, but it works and is intuitive.  I still have my main number answered by a live remote receptionist during working hours, which costs me about $100/month.  I could get rid of that if I wanted.  

The thing about Ring Central is it's easy to scale up or scale down.  No complaints.

*— u/golfpinotnut* | [comment](https://reddit.com/r/LawFirm/comments/1imbiai/_/mc7yvu0)

---

### r/VOIP — 2024-05-11 | 3pts

> VoIP can easily accomplish this. We do it all the time using SIP Trunking (Telnyx, Twilio, VoIP Innovations, etc) and a server running FreePBX. SIP Trunking is where a provider sells a service to connect a computer/server PBX to telephone lines. There are many providers for SIP Trunking and many different hosted PBX platforms, but we find FreePBX to be simple and many features. A PBX is a computer/server/appliance that operates a physical phone system and contains all your programming, to make your extensions/apps/phones connect and pass that on to the SIP Trunking provider. Then we add a mobile app called SangomaTalk (aka Sangoma Connect). There are many softphone/mobile apps that you can use also (Linphone comes to mind if you want a free one or your provider doesn’t have a branded app), but we have found the ease of setup, security, and call quality on SangomaTalk to be superior to others in our testing on our equipment. 

The USA companies I mentioned above also operate internationally and with international numbers, but someone can maybe point you to a German provider than can do the same for a better rate and better matching your needs/taxes/etc. 

However, what you are asking for is extremely simple and should be available in any Cloud PBX offering. A cloud PBX is often sold with the SIP Trunking and PBX together as a single purchase. Everything is in the cloud, so you don’t buy any equipment. And it is priced per extension. 

You need:

1 phone number (often called a DID)
1 inbound route (programs what happens on PBX when DID called - points to ring group)
1 ring group (can ring all extensions simultaneously, sequentially, etc)
3 extensions (this is usually what you pay for when you setup this kind of service $/mo/ext)

Then decide what happens to unanswered calls. This is setup in the ring group. I assume they go to a single voicemail if all 3 extensions miss the call. But the unanswered call could also go to an automated attendant (press 1, 2, 3 system) and then go to multiple voicemails or different places based on the digit pressed by the caller. 

Outbound calls for each extension will just be setup to show your main number. This is called CNAM (caller name and number). Some providers refer to this as caller id masking but that is really an improper use of that term with VoIP and more refers to when people have multiple copper telephone lines. 
3 extensions (and, 3 mobile apps free or licensed)

If the app is proprietary then they will just send you a link to click on and setup is usually automatic. If you use a free app, then you’ll have a server address, username, and password to enter in the app. 

When you receive a call it will ring in the mobile app (this is a SIP client that works just like a desk phone). You would have options like answering calls, transferring between extensions, hold, conference, transfer to outside number, recording, etc. When you place an outbound call you just use the app and people will see your busines

*— u/DigeratiMN* | [comment](https://reddit.com/r/VOIP/comments/1cpew5m/_/l3m6ymb)

---

### r/VOIP — 2024-03-13 | 1pts

> tried dialpad. pretty good site for ai and self help but heard crickets when needed customer service and after they got my credit card, they were done responding to emails and setting me up. i moved to ring central. no call recording on grasshopper and we wanted that. 

i emaild dialpad to cancel (where the website told me to email) and they did not and charged me 91 bucks 3 days after i cancelled. I had to have my cc company create a dispute and not let them bill me again. even the sales number wont answer for dialpad.

*— u/Confident-Mix3337* | [comment](https://reddit.com/r/VOIP/comments/phwui6/_/kuqpnwt)

---

### r/VOIP — 2024-01-18 | 1pts

> We have a small 3 person team. We are constantly on the road so primarily need a service that allows all 3 of us to reliably answer phone calls and text messages.  We started using Google Voice and it worked ok when just 2 of us but had lots of problems with dropped call.  We switched to Ooma Business about a year ago and the calls are much more reliable however lots of issues with texting. Texts don't send, we don't always get notifications, can't see texts sent by another team member, etc.  Not to mention the limit on text storage means we're constantly having to do cleanup.  Too much hassle for the cost of $25/user/month.  In short we need the following to reliably occur:

* One number to ring through to 3 mobile phones
* One number to send and receive text messages on 3 mobile phones
* Voicemail 

All of the other features like schedules, ring groups, fax, etc are nice but not must haves.

*— u/OptimalAssistance124* | [comment](https://reddit.com/r/VOIP/comments/18wpndh/_/kid4np9)

---

### r/agency — 2025-04-03 | 2pts

> The niche is the hardest, so congrats on that. 

An older IT business owner once advised me that I needed to work on finding MRR - that it would change my life. 

I went back to the shop and worked on it for weeks until I figured it out. He was right...it's life changing.

You want three things, huh? Here we go...

1. Rethink why you price projects the way you do. As an example, does your cost to build a website REALLY justify the price you charge? Or are you charging that much because you only have one shot at making money on the thing, and you know you'll have downtime after it's done? Could you lower your price IF you had a 12-month commitment?
2. For work that is naturally project work, don't just spread the project cost out over the duration. That's not MRR. That's more like providing the client a credit-free, interest-free loan they pay off over time. The idea with pricing is that you want to NOT go underwater in the beginning of the engagement while making more money during future months.
3. Start pitching MRR solutions. The longer you pitch projects, the longer you'll be doing only project work. Once you're ready, pitch your offering only as a recurring service with a recurring fee, even if upfront work is required. Clients actually like MRR solutions because they smooth the outbound cash flow and provide predictability. 

Bonus answer:

* You don't have to switch 100% to MRR. Instead, you can charge for obvious project work like building the website and obvious MRR work like hosting and support. Mix and match if you'd like. Some clients will appreciate that because the payments naturally align with the amount of work over time.

I hope that gives you a few things to think about. 

Keep at it. MRR will change your life.

\~ Erik

*— u/erik-j-olson* | [comment](https://reddit.com/r/agency/comments/1jpcit8/_/ml80fdi)

---

### r/agency — 2024-01-12 | 1pts

> Hey Jake, thanks for such a massive breakdown for my question. I love that. Read the answer for almost 3 times and  I appreciate all of the effort and time you took to answer all of my questions.
Before posting this question on reddit. I saw one of your comments on some other posts too which was about building a community for agency owners
I joined to discord channel of this subreddit from that post and also subscribed to your podcast too! Will surely explore that soon

So at first- reason for my starting this agency. Your assumption is partially correct because my goal is to make money. I am currently 19 years old and I am passionate about making money online. I have tried a lot of things before too. I was building websites, I used to sell SEO backlinking services too, then I switched to build operations and project management systems to agencies
But none of then really stick to me because some services were very hard to fulfill like operational systems and some were very commoditized like website design. 

I have recently dropped out from university too and I watch a lot of content on YouTube and the service I am currently providing = lead generation. Really appealed to me because every business needs more leads and if I can have a performance based offer, no one should hesitate in working with me( in my assumption )

That's the reason I have no monetary capital as well to invest in tools. This is the free website I made for my business:

Artileads.typedream.app 

Now, I am trying to find someone whom I can work for on performance basis

And thanks for the giving me access to asking questions from you. That's so kind of you and surely I will reach out to you when I will have any questions.

Thanksss a lot, Jake!

*— u/haroonxh1* | [comment](https://reddit.com/r/agency/comments/194tzjk/_/khirupo)

---

### r/LawFirm — 2024-04-24 | 5pts

> I tried out Call Ruby (a US-based virtual receptionist service).  They were really good, but I cancelled -- let's be real, no one was calling me at the outset.  lol

*— u/Corpshark* | [comment](https://reddit.com/r/LawFirm/comments/1cbj683/_/l115m0s)

---

### r/LawFirm — 2025-07-20 | 1pts | Mentions: **Ruby Receptionist**

> We (small forensic accounting firm) used Ruby Receptionists for years. At first it worked great, but then they basically stopped picking up the phone. We have a low volume of calls and fewer than half of them were being picked up. So I went back to requiring my two assistants pick up the phone. I'm still super annoyed that, despite paying two people to answer the phone, a fair amount of our phone calls don't get answered. There are no good solutions 🤷‍♀️

*— u/auditrix* | [comment](https://reddit.com/r/LawFirm/comments/1m1nj30/_/n463w02)

---

### r/LawFirm — 2025-07-17 | 3pts

> I stopped using it more than a year ago because more than 25% of calls wouldn’t connect. I saw it ring and when I tried to answer, it disconnected the call. Then, the caller wasn’t able to leave a message. It was very frustrating.

*— u/BubbleWrap027* | [comment](https://reddit.com/r/LawFirm/comments/1m1f6su/_/n3lvkbg)

---

### r/consulting — 2025-04-13 | 1pts

> Almost stopped using google. If that helps answer your question

*— u/bigbadwolf2012* | [comment](https://reddit.com/r/consulting/comments/1jvwypu/_/mmxeaak)

---

### r/VOIP — 2024-11-21 | 1pts

> We started with Weave when they were a Beta company. We  thought it was great as our business was growing at the time too. They didnt offer alot of options at the time so we went to a company called solutionreach and that was an awful experience so when our contract was up we jumped ship and went back to weave. We have been with weave for quite sometime. Well the past 5 months the customer service has plummeted down the drain, cannot get a call back, no email back. when we call in the same "Alex" guy answers and transfers us to multiple different people ending in the call either gettting dropped (after 30 minutes) or going back and forth saying someone will call us back. Its bad and i am starting to wonder if the company is tanking. We will not be renewing our service with the come January due to the awful service and poor customer service skills.

*— u/No-Gain4410* | [comment](https://reddit.com/r/VOIP/comments/1djlc3m/_/lyb26fp)

---

### r/LawFirm — 2024-03-22 | 8pts | Mentions: **Smith.ai**

> We dropped Smith.ai for the same reason. The first few client complaints I ignored because I thought “clients can be tough” but after the 4th complaint I realized it was not the clients but actually Smith.ai. We moved to Ruby with no complaints so far.

*— u/Remarkable_Neck_5140* | [comment](https://reddit.com/r/LawFirm/comments/1bl4qtc/_/kw2ryfw)

---

### r/LawFirm — 2024-01-10 | 1pts | Mentions: **Smith.ai, Abby Connect**

> [smith.ai](https://smith.ai) has always been good, even though they seem to be going through change like many agencies do. Don't have much experience with Ruby, but seems to be recommended here so may reach out. Abby Connect seems to have dropped off the planet - can't even get anyone to respond half the time and was not good.

*— u/MyLegalSpace* | [comment](https://reddit.com/r/LawFirm/comments/190sf6s/_/kh8k57w)

---

### r/agency — 2026-01-27 | 2pts

> Hello!   
  
What would your advice be for a 19 year old joining the agency space. I started 6 months ago an agency or ai agency, in uni first year in a foreign country (Netherlands), started selling AI Chatbots and Receptionists and came quickly to the conclusion that I dont need to sell AI, but the outcome.   
  
I’ve tried cold calling, cold DMs, cold email, door 2 door, and my personal network, but haven’t landed a client yet. I don’t speak Dutch, only English and my home language, which made things harder locally. I spent the first 4–5 months focusing on real estate in the Netherlands and had conversations, but repeatedly got ditched.   
  
After that, I switched my offer to lead generation (ads + lead qualification and booking systems) for roofers in the US. At times, I’ve felt unsure whether I’m focusing on the right things or just creating activity without progress.  
  
If you were starting today with zero clients, what would you focus on first, and what would you stop doing immediately?

I should also mention that I have some small social proof: I built two websites from scratch for a small coffee shop and ran ads for it.

I’m not afraid of critique and would genuinely value a raw answer.

Appreciate your time either way.

*— u/Large-Window-5028* | [comment](https://reddit.com/r/agency/comments/1qmzepb/_/o22tgxp)

---

### r/consulting — 2025-03-23 | 1pts

> It would still be MY computer, as in, if I were to leave it would stay with me, but I can understand your point.

The company I left for this one, while not consulting, paid poorly base salaries with bonuses under 3% and would give you any equipment/software you asked for with a shit culture, an HR person who used to be the receptionist and didn't know what the FLSA is or confidentiality, and had red flags planted all over the place. So I'll take the great culture, team that actually works together really well, good salary and great bonus with a dated but new PC with the small but growing company and opportunity of helping them continue to grow 🤷🏽‍♀️

*— u/MidwestSkiQueen* | [comment](https://reddit.com/r/consulting/comments/1ji79bg/_/mjdfk77)

---

### r/agency — 2024-02-18 | 6pts

> All of our clients come to us off of a bad experience with another agency.

They tend to stick around once they see our process product results that positively affect their bottom line.  Our contracts are month to month and can be cancelled anytime without penalty.  Our avg tenure on our client roster is 7 years.

To answer your questions:

The faster I've ever closed a deal was at the end of the initial discovery meeting, when I gave the client a price and he said yes.  We swiped his CC that day in my office.

The slowest?  Probably 6 months.  In my experience, 90 days is pretty typical for our sales cycle and if they drag their feet much longer than that, it's not going to happen.

Purely relying on referrals and the odd cold outreach.  Every single client on our roster is a result of a preexisting relationship.

We don't work with startups so I don't know if interviewing me would be beneficial.  We work with service based companies, specialty retail, ecommerce and manufacturing types of business primarily.

*— u/Moxie_Mike* | [comment](https://reddit.com/r/agency/comments/1ath5r0/_/kqxzkgc)

---

### r/consulting — 2024-05-17 | 9pts

> I decided to respond because my life was changed by doing precisely this. It isn't for everyone, but my desired lifestyle needs autonomy, and it is impossible to get that in a big company, especially as you are climbing the ladder.

1. 8 years ago, I dropped my normal job with vesting in retirement and stock and even gave up my health insurance to start a small consulting firm in an unrelated field.  Consulting on your own puts a much larger portion of your hourly in your pocket, and having a firm puts a portion of your employees' hourly in your pocket, but you are responsible for getting the gigs...

2. 50% of our clients are organic word-of-mouth which took considerable time to build, the other 50% resulting from marketing/direct outreach.  It is industry dependant, but our industry involves highly regulated or otherwise public governmental processes, so our client pool is easy to get data for.

3. Branding is different for an organization than an individual, being a thought leader is important for both.  I like to think of our firm as a brain trust in our field, and i have rounded out our staff around this goal.  I never wanted to be a sole proprietor - you can only crank your hourly so high... and you have to do actual work for every dime you make.  To me, it's better than working at a firm in terms of autonomy but it has a hard cap on revenue.

4. Clients have all sorts of different needs. Our projects are varied, but we typically treat each new project type as a 1-1, and if it can be turned into a repeatable or automatable and marketable process, we make an SOP and if possible convert it to a fixed price deal

5. I never started solo, but with a partner and one employee.  We staffed up pretty quick - as having additional revenue streams for the business makes everything easier and you can eventually afford support staff for admin.  We have had success doing some "lower level" consulting in adjacent areas, preformed by lower paid staff.  It's allowed us to take on more types of projects.

6. Colaboration with other consultants is great, either through a direct collaboration, a pass-through, or just a referral (fee). Just write a good agreement. Around year 4, I noticed that we were referring a lot of the same type of work out to third parties on a regular basis, so I brought in-house any of the services we could reasonably provide, and monetized the referrals going forward.  

Partnerships can be great - and also awful.  Have a good agreement - but that is only 10% of it.  It's a relationship not unlike a marriage.  I have a great situation with now two partners, but we have clearly delineated roles and responsibilities with no overlap and complete autonomy.  They are good humans, we've established extensive rules for governance and decision making, and we have SOP's for every process... and it still gets really shitty sometimes.

7. Make long-term life goals before you make career goals. YMMV.  You have to do some real soul searching.  For 

*— u/white_collar_hipster* | [comment](https://reddit.com/r/consulting/comments/1ctsyyp/_/l4ei2ik)

---

### r/LawFirm — 2025-05-15 | 1pts

> So, I kind of do a hybrid. California family law. I’ve been on my own for about 2.5 years and was at a firm before that. 

I will say that I do zero advertising. I am currently (knock on wood) 100% word of mouth referrals. Back when I was at a firm, we did paid advertising and 100% paid consults. While I didn’t handle the intake calls (we had an office manager for that) I do know that we charged $475 for a 1 hour consult and that a lot of the potential clients from the paid services dropped off when they heard about the cost. Great! Fine. They probably wouldn’t pay anyway. 

Now I usually only do paid consults when I *don’t* know the potential client is coming from a good source. I know the source because, before I speak with anyone ever, I have them fill out an online intake form. The intake form isn’t just for conflict checks but also asks about salary, property and who referred them. If the potential new client refuses to fill it out, fine but we’re not talking unless and until they do. 

That said, I work with a number of entertainment lawyers, real estate lawyers, business managers and the like. Let’s say I did a divorce for Actor A two years ago and Actor A’s entertainment law attorney, John Smith, passed along my contact information to Actor B, who the entertainment lawyer also represents. I might see that Actor B wrote on their intake form that John Smith referred them. I’ll do that call for free because, almost invariably, I’m the only divorce attorney this person wants to bother contacting. Assuming I seem normal on the phone, 9/10 times, they’ll hire me by the end of the call. 

If I don’t know the referral source, I’ll take a look at what the potential client wants and what their resources look like based on answers to the intake questions. In the US, you can very easily look up addresses and home values on Redfin. If they live in a $7M single family home and they want a prenup, I probably won’t charge for a consult, because it’s probably a good case and the call is unlikely to take too much time. They probably just want to talk to someone professional and nice and check that box and be done with it. If I can’t read into the information on the intake form AND I don’t know the referral source, I’ll likely charge. 

All that said, I think those online referral things are absolute shit. You’re probably better off networking with other lawyers and advertising in a hyper local way. Other lawyers are a terrific resource because 1) when people need a family law attorney, they’re likely to ask for a referral from the only lawyer(s) they know and 2) if someone can afford the first lawyer, they can probably afford the second. Try meeting with trusts and estates lawyer, real estate lawyers and small business type lawyers. Get to know them so you’re the first person they’ll recommend when someone calls them and asks for a divorce referral. Secondly, hyper specific local advertising is probably the way I’d go if I did advertising. There’s an eleme

*— u/asophisticatedbitch* | [comment](https://reddit.com/r/LawFirm/comments/1kmca9r/_/msj8vcm)

---

