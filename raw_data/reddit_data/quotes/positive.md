# Verbatim Quotes — Positive

**Source:** Reddit (via Arctic Shift)  
**Collected:** 2026-02-11  
**Status:** Collecting (updates live)

---

### r/LawFirm — 2024-07-26 | 7pts

> I'm an attorney and do IT consulting for lawyers.  We specialize in small practices.  Here are some of the things I have learned over the years.  I have toying with the idea of doing a weekly tech live chat just to answer questions.

* Be prepared to do a lot of business stuff.  I have had a couple small and solos go back in house because they were just "tired of running a business" Others, really love the business part.  It isn't overly complex but it does take up time.  
* Set your tech up right and automate as much as you can.  There are a lot of good posters on this subreddit who give amazing advice.  Gusto for payroll and taxes, FreshBooks for time tracking and payment, QuickBooks online, Office 365 and so on.  Partner up with a good tech support company in your area.  *Make sure they use a program to backup Office365 for you*
* Cashflow is king, so work out how you will bill the client.  Local rules may determine your options.  I take our fee prior to the month of service.  I have seen some firms that will send an invoice and then auto bill a credit card at determined period of time, unless there is a complaint with the invoice.
* Costs and taxes will always be more than you anticipate.  You will have to pay more in taxes than you think.
* Try to get your contacts and mail exported from your old firm.  Partners usually get this.  Your professional contacts will be critical
* Make sure you have thought through your sales pipeline so that you always have new cases coming in.  Most partners leaving firms know their practice and know how to make it rain, so you will probably be fine.

I hope this is helpful.  Good luck, owning a business is amazing but it takes a lot effort.

*— u/LeaningTowerofPeas* | [comment](https://reddit.com/r/LawFirm/comments/1eclctl/_/lf1y5eg)

---

### r/VOIP — 2025-08-01 | 5pts

> For posterity, here is their full comms to customers:




~~~~~~~~~~~~~~~

Dear Customer,

As announced, VoIPo will be ceasing operations effective August 6th, 2025 at 11:59PM EST.

Our top priority is to make sure that you have minimal disruption and that your phone number is easily transferred to a new provider. We highly recommend VoIP.ms, an established telecommunications provider with over 15 years of experience with residential and business phone systems, as well as VoIP resellers. The VoIP.ms team is ready to help and has taken several steps to make sure things are seamless for you. We believe VoIP.ms will provide you with excellent service, customer support, and competitive rates.

With that said, we understand you might have pressing questions concerning your account, the reason we are shutting down operations and billing issues. We have prepared some questions and answers we believe are more urgent concerning this matter.

 

General Questions

Q: Why is VoIPo ceasing operations? 

A: Due to challenging market conditions, significant financial losses, and a key vendor disrupting our ability to process credit cards or issue refunds, we can no longer operate. This was a hard and difficult decision made after exploring all available options.

Q: When exactly does my VoIPo service end?

A: All VoIPo telecommunications services will permanently cease on August 6th, 2025 at 11:59PM EST.

Q: What if I have billing or other questions about my old VoIPo account?

A: VoIPo will provide limited support through closing via e-mail at support@voipo.com.

Q: When should I start migrating to another provider?

A: Immediately. The sooner you begin, the smoother your transition will be, otherwise you might suffer longer service interruptions.

Q: What do I do with my VoIPo adapter?

A: VoIPo is not requiring the return of any equipment. You may use the equipment with VoIP.ms (or any other provider) if they support it or dispose of/recycle it.

 

Migration to VoIP.ms Questions

Q: Can VoIP.ms access my VoIPo account to help?

A: No. VoIP.ms cannot access your VoIPo account information or resolve VoIPo-related issues.

Q: Why is VoIPo recommending VoIP.ms?

A: VoIP.ms is a well-established provider with over 15 years of experience with residential and business phone systems, as well as VoIP resellers, excellent service quality, competitive pricing, and the technical capability to handle VoIPo customer migrations smoothly. Learn more about VoIP.ms right here: https://migration.voip.ms/voipo.

Q: Will VoIP.ms honor VoIPo's rates/contracts?

A: No. VoIP.ms operates independently with their own pricing and terms. However, their rates are competitive and often lower than industry standards. See https://wiki.voip.ms/article/Service_Cost and https://voip.ms/pricing. 

Q: Will my current equipment work with VoIP.ms?

A: Most equipment will work with VoIP.ms, but will need reconfiguration (ie. factory reset). VoIP.ms built this extensive knowledgebase article to h

*— u/s0f4r* | [comment](https://reddit.com/r/VOIP/comments/1mezs0r/_/n6eb9jg)

---

### r/VOIP — 2024-07-18 | 2pts

> To address your first part, theyre all on the same switch. The way our network is set up is we have every CAT5 cable coming down a pipe in the cieling that goes into a patch panel on our track, then from the patch panel into two Netgear switches (oddly, all phones just happen to be on our top netgear switch, just somehow worked out that way to use the PoE function), then from the switches, it goes into a Ubiquiti Edge Router X, then to our Fiber ONT (which is in bridge mode so I can control the network better via the Edge Router X). So ill poke around in the Edge router to see if there is any multicasting configuratings I can set up to get that working. Looking around on the further with the VOIP Server we are using, they do not seem to have anything on their end for that and their tech support DID tell us - its something where the phones need to be configured for that - not the server side. So it would have the be the latter to take a look into.

  
For the second part of your comment, same answer from the VOIP service - it has to be set up via the phones, not the server side. The DND function IS native to the phone. The 3rd menu function button on all phones is "DND".  Now, how you explained it on the server side of things - this is exactly what I figured what was going on. I put my phone in DND, and no other phone sees it, my thought was "Well, the server isnt TELLING the other phones "That person is in DND right now" because...it doesnt know. Its not sending that information of DND from the phone, to the server, then back to our location to tell the other 3 phones. But this is where I get confused because it DOES WORK as far as being on calls or being free. The server is clearly telling the other 3 phones, that 1 phone is currently on the line with someone. So why DND won't work? Puzzling me - which prompted me to come here to ask "What on earth is going on!?" LOL 

Now, I did leave something out in my OP that I felt wasn't necessary, but maybe itll help work out in the end. We recently switched ISPs. We were using Comcast for years with traditional cable internet/phone and we wanted fiber. Not to digress too much here but Comcast was our only option here in our industrial complex because the landlords son apparently had some relationship to comcast and wouldnt allow another ISP? IDK, even the landlord was like "um what? Im not aware of that" but who knows, thats what this NEW ISP told us which is a Fiber ISP (Bluestream Fiber, I use them for residential and theyre amazing and their tech support is great I can nerd out to shit with them). Enough digressing, this is what prompted us to move our phone systems to this. Our final set up appointment is tomorrow. We did decline to use one of their phones they would lease to use which was Polyfon? (probably spelt that wrong), we wanted more options and they said any VOIP phone works and it saves money on the bill if you just buy your own. Ill be honest, these Fanvils are AWESOME in my opinion. The s

*— u/Kaotix_Music* | [comment](https://reddit.com/r/VOIP/comments/1e5sz41/_/lds7x30)

---

### r/agency — 2024-03-19 | 1pts

> I've been using HighLevel for a few years now and I love it. 

It is primarily for agencies to use as the back end automation for their clients. It has everything from scheduling, a homegrown website/funnel builder (better than Clickfunnels IMO), text and email automation, they are even developing a service that can replace Zapier in some instances. Oh yeah, and wordpress hosting too. Oh, and social media posts and scheduling. ...and google my business comment replies...

Honestly, I can't even remember all of the features because there are so many, haha!

And to answer your question, yes, you can whitelabel it with your own brand and domain. They even have a SaaS mode where you can whitelabel billing, etc. Happy to answer any questions about it - but I highly recommend it. It replaces so many different tools it practically pays for itself.

*— u/BurntAlgae* | [comment](https://reddit.com/r/agency/comments/17igse3/_/kvkw0ro)

---

### r/LawFirm — 2025-12-05 | 1pts

> You have two options:

1. You build a call center in-house

2. You use a call answering service

Obviously, if you're a solo attorney, you're not building the call center in-house because it's expensive, cumbersome, and takes a long time.

Highly recommend using an answering service that works specifically with law firms and understands intake. The one I use is called InsideOut Law Calls.

*— u/lnsknndy* | [comment](https://reddit.com/r/LawFirm/comments/1kipywo/_/nseceef)

---

### r/LawFirm — 2025-10-11 | 14pts

> As a new (~1 year) paralegal, who is 55 years old and has three other careers behind me, this is great advice. 

There are ABSOLUTELY some things about being a lawyer (or in the legal profession) that are different from "other" jobs, but the basics of honesty, career development, work-life balance, "good boss/bad boss", etc. are universal. 

1) "Work from home/hybrid/chained to a desk at the office" are UNIVERSAL questions in the workplace. Don't let anyone lie to you about their expectations. 

2) My SAs are amazing in their "support" of me, so I "support" them back with equal passion and zeal. So *together* we've managed to hit some impossible deadlines and sometimes triumph on behalf of our clients. They are as respectful of my abilities and limits as I am of theirs. I wouldn't work for someone (attorney or not) who didn't respect their need to support me. That is the "price" of loyalty. 

3) I have been handed a task and told "go." BUT, along with that, the guidance to figure the shit out, and the acknowledgment that my first draft wouldn't be perfect. The best part of my training is when my SAs answer my questions with "here is where you can look this up" instead of annoyance. It makes me smarter and more capable, and also reflects that THAT is what they want.

4) To quote:

> "I've only been litigating a year and have no idea what I'm doing. It's a whole new area of law for me."

As a newb to the legal field, the biggest shock for me was learning that my SAs (both of whom I consider to be among the smartest, most ethical, and kindest humans I have had the privilege to know)... don't think they know shit. 

They are ALWAYS looking things up, NEVER assuming they "know what they are doing." Both are litigators. Litigation is, by definition, NEVER the same thing twice in a row. My opinion on this matter is worth fuck-all, but you asked the question, so my answer is: if you don't love it being new where you don't know what you're doing, *but can do it with the right support and time and love*, don't litigate. But that is YOUR choice. I f'ing love the fact that my last career will be filled with learning new skills until I'm too mentally weak to learn more. Then I'll die happily. But, that's me. Your mileage may vary.

5) To quote, again:

> (cue panic attack today crying in my office)

I "retired" from being a professional chef to focus on being a paralegal. There's a well-known phrase in the restaurant industry about "crying in the walk-in" which means going into a big-ass refrigerator and closing the door before you let loose on those excess emotions. The reason it's a trope is that... well... e-v-e-r-y-o-n-e has done it, and instead of thinking overwhelming emotions are "toxic", the food service community accepts it is part of life.

It's 10X that in the legal community, but somehow some/most of y'all don't simply accept that. What you do as lawyers is passionate, HARD, taxing, challenging work. And YOU have to accept the responsibility for s

*— u/retailguypdx* | [comment](https://reddit.com/r/LawFirm/comments/1o3921w/_/nivninz)

---

### r/legaltech — 2026-01-31 | 18pts

> I wrote this a few months ago. Still generally true, so posting it below. But a couple of minor updates:

- feel like the customer support is regressing - maybe related to them signing up too many customers without equivalently growing their customer support team.
- they keep talking about having some kind of secret sauce behind how they choose the right llm in responding to queries, but it has been difficult getting substantial details about that. Hopefully in the near future. Related to the above point. 

-----

I agree with some of this, and disagree with some of this. I use Harvey regularly, and have done so for the last 12-ish months. I'm at a non-US firm with about 5000 people worldwide. 

AGREE
- Harvey is a wrapper. They seem to have given up on substantially "tuning" the models that they use. They just announced that they are making available Claude and Gemini (in addition to GPT) - Expanding Harvey's Model Offerings

I don't necessarily see this as a negative. My general view of LLMs is that they will become commoditised, and the value will be in the layer(s) that sit on top of the LLM - there are so many good LLMs now. 

- Harvey is expensive. We got a substantial discount in the first couple of years for getting an enterprise licence. But it'll become very expensive (I don't have the exact figure, but USD1000/seat/month sounds about right for a rack rate). So if I was running my own firm or part of a small firm, I wouldn't look at Harvey for that reason alone - there's too much competition out there, whether from foundation models or from wrapper companies. 

- A lot of Harvey is hype. They clearly have a very solid, dedicated marketing / PR team. They do interviews with the right crowd, their blogs are very polished, and their founder's public messaging always stay on point. I mean... it's Silicon Valley. 

- I have generally been unimpressed thus far with the workflows. They have just introduced a "customs workflows" feature for building my own workflows, and a "playbooks" feature for building playbooks based on existing documents. Both of these have have some promise, but I need to test them more to have a strong view either way. 

DISAGREE
- I have found Harvey useful - so I disagree with OP's general negativity about the product.

It is definitely not perfect. But a couple of comments there:

(1) It has improved massively since I first tried it in 2023. My view (that I told my firm about) at the time was that Harvey was crap, and we shouldn't get it until it improved massively. I also think when they first started out, they tried too hard at tuning (see above). 

(2) There are three main positives about Harvey that I see now. 
1 - the wrapper is straightforward, simple and easy to use - this is a very big deal for busy lawyers who don't want to deal with crap interfaces. 
2- the output is generally good. At an individual level - document summarisation, BD article preparation, short advice writing, sense checking answers, bouncing

*— u/h-888* | [comment](https://reddit.com/r/legaltech/comments/1qrio2s/_/o2qingo)

---

### r/LawFirm — 2025-01-03 | 2pts

> What you are describing (at least to me) does not sound like a CRM exactly, more like a practice management tool (and there are MANY). I feel like most tools are geared towards PI (bigger money, larger firms, etc) so you will have plenty of options.

When I think of a CRM tool, I think about that as being something working hand-in-hand with marketing, following up on leads, prospective clients, doing follow up to book consultations (also sending reminders of upcoming appointments) and then taking the lead to "client" status.

I have used a few different tools trying to find the one that worked for me (high-volume solo criminal in Chicago). I tried Clio (hated how many steps I needed to go through to create files and a discovery soldering system which did not appear to have been fixed some three years after I left them) and Clio is about as big a name in the industry as there is. They were huge on being early adopters of integrations with other tools (something I tip my cap to). I then went to Smokeball, which I liked a lot, but at the time didn't have a Mac option, no application for my phone, limited integrations (I see now far more integrations which is great). I then moved to MyCase which was quite good and the recommendation I would make for most people. Certain levels of customization to make it your own, all the tools I would trust firms would need, PC/Mac applications and plugins, they really upped their integrations up as well. What I ran into as an issue was they had a data size cap for individual files (1GB) I routinely have files that go above that and I was stuck uploading to a Google Drive for random large files rather than having my complete file together.

I am currently with Filevine which is the most daunting, but also most customizable option there is. There are upfront costs with them that arent required with other such software, but you really can make it "your own" from layout to what sections are called and what order things appear (along with required data to be entered, etc.) but it can take serious time and not insignificant money (2,500-5000 id suspect) to get you off the ground on top of the fees for the base software itself. I do love it and continue to learn and hone the software further for document automation, AI tools that Filevine I feel is at the forefront with, etc.

For true "CRM" as I defined above, there are many of companies that offer similar tools, for a more legal focused version: Lawmatics, LeadDocket, LawRuler. I used the first two. There are companies that then white label Go High Level as a CRM tool (LawHustle as an example). I ended up going to Go HIgh Level and finding a guy through Fiverr who had GHL experience to build out my own tool, with my own workflows while not having to pay a different company a monthly premium to use the tool I can get to on my own. I am VERY excited about how the tool will work for following up with leads via email, text, voicemails, an AI Chatbot coached on my website an

*— u/ElderberryAny1806* | [comment](https://reddit.com/r/LawFirm/comments/1hrw62q/_/m54z8io)

---

### r/LawFirm — 2025-07-14 | 2pts

> For almost any task, you can either pay someone to take it off your hands, or automate it.

Whether you can do so ethically, affordably, and maintaining sufficient quality, is a different matter.

I think practice management software like smokeball, mycase, PracticePanther and Clio Manage are absolutely worth the price just for the organization alone, and they include extra quality of life like escrow management, electronic signature, automated workflow, and document automation.  How much benefit you get depends on how much effort you put into setting it up and making sure you use it properly

Depending on your field, there may be dedicated drafting software.  Do not use AI drafting, there’s too big a chance of having mistakes, missing something important, or generating a hallucinations - not to mention issues regarding client confidentiality; do not ever put in identifying information.  You can use AI to help create an outline or rewrite a paragraph, but treat it as a dishonest college student who would rather make things up, and will insist on being right even if it’s wrong.

Then there’s CRM like Lawmatics and Clio Grow.  This helps manage your marketing and client intake.  But it still requires time and effort on your part, and might not help you all that much.  

A paralegal can do a lot of grunt work, and if you don’t want to commit to a full time employee, you can hire a virtual paralegal (paid by the hour)

You can get a receptionist, a chatbot, or an answering service to answer calls and/or chats on your website.  The quality will never be the same as what you can deliver

Bookkeeping you can and probably should get software, but that still takes up a lot of time.  The best thing you can do is hire an actual bookkeeper, they’re cheap enough.

It is possible to create a fully automated process where a client fills out a form or questionnaire online and documents are automatically created.  That has two drawbacks: (1) your client doesn’t see the difference between you and legalzoom or rocketlawyer and they’ll wonder why they’re paying you.  (2) your clients will make mistakes in entering their information, and may select the wrong options if you let them.  I won’t do it, people pay me a premium price for a premium service and I want to make sure it’s done right

*— u/Dingbatdingbat* | [comment](https://reddit.com/r/LawFirm/comments/1lz9h1y/_/n31ro38)

---

### r/agency — 2024-03-10 | 2pts

> I tell them the SEO industry is full of snake oil salesman and scammers. It’s a Wild West out there and anyone can be anything. The best way to filter them out is if anyone claims they can get you to the first page of Google in a few months they are a scammer because it doesn’t work that way. It takes time and lots of work to do it. We need to build authority with Google and have lots of content on our site that answers our customers questions and satisfies their searches. Or if you ask someone what they’d do for SEO work and you’re given a bunch if buzzwords that you never heard of before or understand, they’re a scammer. Real SEO people want you to know exactly what they’re doing, what it does, why it matters, and how it works. They don’t hide behind obscurity. They are open and thorough with a set plan and proven results form happy clients you can contact as a reference. When they ask me what my SEO guy does, I tell them this:

SEO consists of 2 parts - on page SEO and off page SEO. 

On page SEO are things you can do on the site itself. Like the design, content, load times, accessibility, blogging, etc. 

Off page are things you do off the site. Like building backlinks to your site; citations, social media, guest posting on blogs, etc. 

Together these comprise your SEO strategy. I am good at on page stuff like accessibility for screen readers and design and load times. My sites score 100/100 page speed score from google. Google likes my sites because they load instantly on mobile and we get extra ranking online because of it. My SEO partner Adam does the content, backlinks, curations, blogging, ads, etc. so my work in his hands makes a complete SEO strategy to regularly create relevant content about your services and building them efficiently so they load fast and make google happy. 

SEO is not a short term flip of a switch and your ranking front page. It takes 6-12 months to see the effects of good SEO strategy. It’s a long term investment. For short term gains you run google ads to show up in relevant searches at the top and get seen by your clients at the point they’re looking for your services. 

So SEO + ads + social media management is what makes a complete marketing strategy to maximize your reach online and be seen my as many customers online as possible. 

If you don’t have an SEO guy or a budget for my SEO guy, What I do is I do searches for my clients keywords in large city metro areas in a different state and open all the top ranking sites. I analyze the keywords they’re using and content, feed it into chatGPT and have it write new content based on that content from those pages and to pretend it’s a copywriter for websites. Then it gives me the content, I edit it to make it sound more human or change sentence structure, and add it to the site. I know what sections I need on a site and what order and what content I need and where to put the keywords. I do this for interior service pages called content silos as well. These content

*— u/Citrous_Oyster* | [comment](https://reddit.com/r/agency/comments/1bb3qiq/_/ku6z2zo)

---

### r/LawFirm — 2024-09-25 | 5pts

> Here are some tech things that help our clients that should help you too.

1. Do your payroll through Gusto.  It is super easy, cost effective, and they will do all your filings.  They will make it easier to onboard new employees and do their filings as well

2. One of the best things I ever did to fix my scheduling is to start using calendly.  It syncs to your calendar and blocks off meeting times accordingly.  I usually block off the first and last hours of the day to make sure I have time to get things done

3. Stop sending gifts to lawyers, it never yields business.  Send them referrals and build your referral network.  The vast majority of my successful PI clients will farm out most everything but keep the solid cases.

4. If you aren't already, get QuickBooks online.  Make sure to flag your expenses each day.  This will help you understand your cashflow.  The two biggest issues most small businesses, PI firms in particular, is managing cashflow and intake.  Focus on those two things and cut what you can.  After my first year in business, I learned that I spent nearly $1200 on coffee.  So, I bought a coffee pot for the office.  

5. As to secretarial staff, there is an obsession with a lot of lawyers that they need someone to answer the phone.  You don't.  Everyone expects an auto attendant.  Let your Ringcentral app work for you.  If you are going to get staff, look for someone who can take care of the 100 little things that need to be done each day.  If they can answer the phone too that is a bonus.

6. Check with your local bar association to see if they have a lawyer referral program.  Look at local legal non profits and develop relationships with them if possible.  They are a great referral partner.

Good luck and hang in there.

*— u/LeaningTowerofPeas* | [comment](https://reddit.com/r/LawFirm/comments/1fp8urh/_/lowtqxk)

---

### r/LawFirm — 2023-07-30 | 239pts

> Finally, THE question I'm qualified to answer! My life has been leading up to this moment. I'm going to drone on a little here...  
  
I left ATC to become a lawyer. I'm obviously a lot older than you; my first day at the academy was in 1982 on the one-year anniversary of the PATCO strike, and I too was a controller in LA, ending up at what used to be LA TRACON on Imperial Highway. I was an excellent controller but frustrated with the culture.  
  
I graduated from a great law school two months after my 40th birthday and found that being a 40-year-old lawyer with no legal experience was not something that anybody was interested in. When I left the FAA, I was married with two preschoolers, and after putting all of us through the ordeal of getting a law degree, to find myself unattractive to employers was crushing. I've now been practicing for 25 years or so and although there was a sweet spot in there where I had enough experience and was young enough to be an attractive hire, I'm now in a position where my LinkedIn profile picture says that I'm too old even though my experience blows away a job description. I'm competing against other people with 25 years of experience who aren't even 50. I want work but I'm having trouble finding it.  
  
Hindsight being 20/20 I would have been better off sticking with ATC until retirement. I would have retired 15 years ago, my FAA retirement would have been higher than my salary as a lawyer is right now (which is the most absurd part of the entire exercise), and honestly, it turns out that I really enjoyed working the ATC problems every day. There are intangibles that still make me glad I left--I'm well respected in the field in which I work, I stopped drinking, and I became 95% less of an asshole than I was back then. But man, it's tough. Although, at your age, getting hired as a prosecutor is more likely than being hired at a firm and you'll want to look at Assistant US Attorney positions to see if your FAA time will go toward your federal retirement from the DOJ. But don't think for a minute that you're going to stop waking up every morning and thinking, "This is unsustainable," just because you stopped being a controller.   
  
Don't sell yourself short in your current career. If you're good at your job and empathetic, you ARE helping people. You've forgotten that what you're doing so effortlessly is quite an amazing thing, and it's OK to bask in that a little. It's impossible to see it from where you sit, but you're making a huge difference in people's lives.  
  
I live in a city with a population of over a million. Although LA County pays much better, the pay range for a city/county prosecutor here is $88K to $118K and the average home price last month was $1.3 million. Be really honest with yourself as you go down this road.

*— u/cctdad* | [comment](https://reddit.com/r/LawFirm/comments/15ddbn0/_/ju1wwiz)

---

### r/agency — 2024-02-02 | 1pts

> Greetings,  
Firstly, I want to thank you, not many people are willing to help me there, but let's get straight into it.  
My offer is running Meta & Twitter ads with a guarantee of money back.  
My niche is Health & Beauty. I mainly reach out to plastic surgery, dental clinics, and skincare brands.  Planning on either trying the martial arts equipment or the insurance nieche.   
Is any of these a good idea? Should I ditch them all and think of a new one? If yes, have you got any idea?  
My outreach methods -  
Sending an email to a brand, ( Have 4 templates they will be included down below ) and wait for an answer. I've seen that you recommended that I shouldn't use my domain email, so I do 50% domain and 50% Gmail. Wait 2-3 weeks and message the brand on Instagram. ( I will try to reach the owners now that you recommended too ). I have sent out about 550 cold emails now, but I got about 5 responses and none of them wanted to go through with anything. I have messaged about 400 brands on Instagram, and the results are way better there. About 1 in 25 brands are interested in my proposition, but after I explain it to them, they just stop answering. This is the furthest I got in half a year.  
I would try cold calling, but that isn't really an option for me. Where I live, it is insanely expensive to call numbers in the US and the UK.  
I also post on Instagram, would you mind checking it? @ kaloroadvertising  
I use snov.io, Hunter, and Anymailfinder to find emails. A lot of times I can only find info, support, etc. kind of mail. Should I even message those emails? Is there any point of that?  
This is everything I have for now. I know it is a lot, but I would be really grateful if you could help me with any of these.  
If you think I should do some other kind of outreach, please let me know!  
Here are the templates, please tell me what can I improve!  
Subject Lines: sometimes insert x!4 or their name before the lines  
"Change this ASAP" "This has to change" "Hello xxx" "You have to change this" "You NEED this"   
A,  
I’m not going to lie, your creatives are wonderful.  
I absolutely love them.  
While I was on your website, I noticed you have Pixel installed and you run ads too.  
I went ahead and checked them.  
I will be honest with you, I have seen a bunch of mistakes.  
You’re losing out on a bunch of money and brand awareness by not marketing properly.  
You’re on the right track, but you have to do it properly.  
We guarantee 2x better results otherwise, we will provide you with a full refund.  
When will you take the first step?  
Book a Free 20-minute Discovery Call with me, so we can get to know each other more,  
and explain how we operate. After that, we’ll see if we’re a good fit.   
DISCOVERY CALL  
Speak soon,  
XXX  
B,  
I absolutely love your website.  
Simple but elegant.  
While I was on your website, I noticed you have Pixel installed, but you don’t run ads.  
Why is this?  
You’re losing out on a bunch of money and brand aw

*— u/ExcitementFragrant32* | [comment](https://reddit.com/r/agency/comments/1afxhp6/_/kolpqxi)

---

### r/consulting — 2024-11-04 | 2pts

> Ha ha ha!!!   
LOVE IT !!   
Yes,.... sorry... IMPOSTER syndrome NEVER goes away, sorry again.... Anyone saying otherwise is either lying thru their teeth or have otherwise really bad introspective abilities....  
20+ yrs counting and YES, I still feel like a "boy in his pyjamas" sometimes...does not go away...   
And YES it's a sign of a well developed ego, a sound mind !! You just have to live with it :-)

To deal with it:  
\- Be humble, always....  
\- Show respect for others and to be frank "there are no stupid questions, only stupid answers" and use that phrase often, ask "stupid" questions... I have no numbers on the meets I've attended where everyone throws around TLA's (Three Letter Abbrevations) which makes everyone feel "dumb" to not know....  
Holy hell STOP playing "smart asses", use clear language.... Because everyone going along on that game is a bloody moron..... Sigh...I get opinionated, sorry....  
\- Be confident in that you probably and in most cases are just as smart as the other guys in the room, and you are smarter than them if you dare to show your lack of knowledge with a questioning air....

Managing others:  
\- Trust .... Trust in them and their knowledge, you are managing, it does NOT imply that you are smarter than them or should know all they do....You are managing to take away their obstacles, clear the path, and provide support for THEIR opinions... RELY on them and show them that YOU care and are willing to stick YOU neck out for THEM....Then they will have YOUR back and fill all your gaps of knowledge.... Just a tip!!!

*— u/eightballyess* | [comment](https://reddit.com/r/consulting/comments/1gitijw/_/lvei8lb)

---

### r/consulting — 2024-08-19 | 43pts

> Day one:
- get the team started on no-brainer activities like booking expert calls, pulling secondary, etc. Anything interesting they see while doing this they should quickly throw on a slide 
- while they are doing that, write a bullet point storyline (one bullet per slide) based on the questions in the scope. One to three slides per question. For each slide state the tagline and enough description of the content you expect to see that a junior person will probably at least sorta do it right 
- pull the team back together mid day. Talk through your storyline, make sure each person sees where their work stream connects to it and what content they're responsible for. Get any slides anyone made as they did startup, talk about them with the team. 
- the team should be expected to improve the storyline with you as you talk it through 
- send storyline to the partner, verbally talk through it with them sometime on the first day 
- end of day deliverable from the team is a blank deck matching the storyline, with whatever content they've come across on the page (could just be a pasted chart to clean up later, or a random quote from an analyst report
- try to get 1-2 expert calls, join them personally so you learn dumb stuff like how to pronounce the names of the companies, and can get a hypothesis in your mind
- set up time with the direct partner in charge every day, and with the senior partner included two days before each client update.

Day two:
- when you wake up you should have a blank deck in your inbox from the team. Read through each page, make comments, edits, give guidance where the storyline was unclear. Call out what you expect at the end of the day - more quotes on this page, an initial market size page, whatever.
- when the team arrives they should have this marked up pack in their inbox. Talk it through with each of them 1:1, answer any questions, ask them for clarification, etc. Don't let them leave until they can describe to you specifically what they're going to go do. Make sure they understand that the instant things stop going as you've agreed, they need to come back to you for help.
- now the team should be good for a few hours. Use this time to handle process (scheduling, etc.), check in with the partner, and get smarter yourself (read the CIM more carefully, read a good market report, whatever)
- pull the team back together mid afternoon and talk through what each person has learned, how that changes the answer, and explicitly what they will deliver at the end of the day.
- brief the partner on the above
- go home, have dinner, touch grass
- check in with each team member remotely after dinner - make sure things are on track, get a firm commitment about what they'll send you and when. If the "when" is like 2am, pare back the work until they are doing something sane.
- the above cadence is what you'll repeat every day

Day 3
- same basic cadence as day 2 (team starts with a marked up deck, etc.)
- deck needs to go to the partner t

*— u/Kingcanute99* | [comment](https://reddit.com/r/consulting/comments/1evi9vm/_/lit7792)

---

### r/LawFirm — 2024-04-04 | 6pts | Mentions: **Smith.ai**

> I used [Smith.ai](http://Smith.ai) - they were fine, but very new when I used them (2014-2015 I think). The main issue is that the receptionists were work from home, so call quality and background noise.

Then I used Gabbyville - they were good too, and I don't really remember why I left.

Finally, I used Ruby.  I highly, highly recommend. They were a bit more expensive, but well worth the cost. Plus they really tried to be one of the team (at least twice I said direct my calls to voicemail because I was ill, and they would send me a care package).

*— u/anne611* | [comment](https://reddit.com/r/LawFirm/comments/1bvnhk0/_/ky0ttej)

---

### r/consulting — 2025-01-13 | 3pts

> Any money spent on HR is less money available to pay overhead or salary for those employees.
If it's a small main street type restaurant, deli business usually they don't have much, or don't like to spend on labor. 
Think about the conversation with a business owner. How would you sell? What would be the reply from the business owner.

In my previous life, I managed a gas station, c store, rental apartments, etc. Revenue around 5mil annually. Paying employees decent wage or hiring adequate help was always an uphill battle. I had a board that I answered regarding operations. The board, or a business owner, refused to acknowledge how spending money on training, paying above the market, and better benefits would attract the best talent from neighboring businesses. 

This will allow us to form a team of memebers who are the best in what they do. Simple correct, you see the point. I see it. Everyone on this sub will also agree with what I wrote. But the board of partners, or in your case, a business owner refused to see value in hiring enough help or employing the best talent. I could not make them see it. Or they saw it but didn't agree with the benefit it provided compared to cost.

The conversation went like this.
Me - If we pay the best dollars we will attract the best talent and employees. Our customer service will go up, less turnover, also by attracting the best employees you are leaving other businesses at a disadvantage. Their employees will be second in competition. Look around us, all fortune 500 always assemble an awesome team. It's the bedrock of a successful business. You pay me top dollars and reap the rewards. We post increasing profit year after year. You give me amazing reviews. If we raise our comp by 20 percent, you can have a team that matches my work ethic and skill. Driven to make this business a success.

Answer- How will we measure that. Paying more doesn't guarantee the best employee. People come for the lowest gas price, good cook and food. They don't come here for cashier. We are happy with our profit now. It has worked like this for years. 

I left after failing to assemble a team that I wished. Having one or two great employees and the rest who have no interest in working for you leaves all the work and responsibility on those two employees. Takes the fun and your passion out. The team doesn't share your passion or care for the success of business.

So I quit. Now, I am in public accounting. Surrounded by talented people. Amazing mentors and coaches. I tried to build this in my existing job. Replicate this model for a small business. Just like you, I envisioned the benefit of mimicking strategies of Fortune 500 for small businesses and failed to let the owners see my vision. 

I hope you succeed. My advice is that small businesses are always run with short term view in mind, scarcity mentality no matter how profitable you are. The business owner does not plan for 5 or 10 years down the road. The business owner doesn't bel

*— u/Necessary_Classic960* | [comment](https://reddit.com/r/consulting/comments/1i0c7we/_/m6wurtv)

---

### r/consulting — 2024-06-24 | 10pts

> Road warrior here. I’ve been doing this now for a little over 12 years and I actually really love it. I’m lucky enough that I get to choose my own destiny and control most of how and where I travel (but not always). A few things that I do to help keep it interesting - YMMV.   
  
• Early flights only where possible. No red eyes and then straight to a meeting in the morning, If international, fly in a day earlier even if you have to pay for it yourself. These flights tend to have the most well behaved passengers and the first flights in the morning usually get priority and won't have backups.   
  
• Going to somewhere cool? (Tokyo, Stockholm, Melbourne, etc...) - get there 2 days early and make time for yourself. See the city. Take public transport. Buy local. 

• Subscribe to Monocle magazine. It's not only chock full of great content but will tell you where to shop for cool stuff and takes forever to read. It's a nice change from the usual nonsense on the plane if you want to spare some time working on that deck. 

• Find and buy one really cool thing from each city you go to. At the end of the year, you should have a collection of cool shit where each piece tells a story.   
  
• Never fly in for a meeting and then head directly to the airport to fly back right after.    
  
• Choose 2-3 airlines, stick with them as much as you can.   
  
• Collect points and rewards on everything on your personal account - NOT CORPORATE. No sharing with your team or account. Sometimes you can sneak this, sometimes you can't.   
  
• Let client pay for your economy class flight - you pay for upgrades. Never fly economy and always get the rewards. Economy is for the common people. You are not a common person.   
  
• Non-stop flights only. Multi-route stops to save money is the devil. Alternatively, know when it makes sense to fly into a nearby airport and then rent a car and drive to your destination. If you have time, it can make it a lot more fun and you can take meetings/calls in the car (eg: Going to Reno? Fly into SFO and drive through Tahoe and Carson City)  
  
• Rent from Sixt where you can. They have great customer service and excellent cars. I would also suggest trying out European brands in the EU if you can - way more fun to grab a Renault, Skoda or Citroen than a Ford.   
  
• One hotel chain (mine is Marriott) and try to stay in the same hotels as much as you can. Get to know the staff. Your goal is to know the names of the receptionists and servers and have them know you well enough to ask about your kids/significant others or pets. You'll not only get perks but you'll be able to time your arrival from the airport/train much easier than if you've never done it before.   
  
• Have a routine. I have routines down to the second at JFK, AUS, LAX, SEA, SFO and MDW. I know the gates, how long it will take to get through TSA and where to eat to ensure I get to the gate as early as I can.   
  
• Know when to break the routine. If you’re going to a com

*— u/yourlicorceismine* | [comment](https://reddit.com/r/consulting/comments/1dnlvut/_/la4emwf)

---

### r/LawFirm — 2025-08-10 | 2pts

> Could not agree more, don't mix messages. Focus more on the PI website and immediately start working with a company to help you optimize SEO.  It will take you a long time to see results but you'll quickly learn how much more profitable a direct in case is versus a referred in case.  

There are a lot of charlatans in the SEO space it's taking us years to find a reputable company, and even they aren't perfect.

Unless you have an unlimited trust fund, you'll never be able to compete with the big marketers in your area. There are probably multiple firms with eight figure marketing budgets.  You have to figure out where they've left gaps in their coverage and paint those corners.  Make sure your personal network knows what you do.   Your style is your style, but there are ways to remind your Facebook friends what you do (posting about a hearing or interesting details about a specific case, check in at your state bureau of investigation when you take a medical examiners's deposition) without coming across as an ambulance chaser.   

Figure out how AI can help you .  I'm no expert, but it's amazing how much time the upgraded ChatGPT account has saved me.   By no means is it perfect and be careful for legal research, but proofreading briefs and stylistic improvements can be amazing.  Upload your motion and the defendants responses, provide other helpful details like depositions, and let GPT brainstorm creative arguments or pour out inconsistencies in the defendants briefing, etc. Just make sure to check everything before you cite.  Spend time creating good prompts and you can easily summarize depositions or create timelines etc.

Try to share Office space with other personal injury firms if possible. It's amazing how many successful strategies we've developed were ideas of other attorneys shared during an encounter in the hallway 

If you don't already, get an assistant or paralegal ASAP. Both for optics (who wants a lawyer who answers their own phone) and because your time is much more valuable generating business or closing out your cases than licking stamps and sending letters .  

Finally, get a good bookkeeper ASAP. Don't waste your time doing quick book entries unless you have significant bookkeeping/accounting experience. Trust accounts are no joke and you can get in big Doodoo if you mess that up, even innocently.

Enjoy!   I started with no cases and an $800 HP computer attached to a dropbox account – now we have a 20 person Firm and handle 7 to 9 figure cases.   I say that not to brag but as context for this statement: the most enjoyable years in my career were the first 3 to 5 of the firm when we were building the Firm and trying to figure it out.   Of all the recoveries over the years, the most memorable was that first million dollar settlement, which felt like proof of concept for us.    It's a ton of fun!

*— u/BiminiBlues-1* | [comment](https://reddit.com/r/LawFirm/comments/1mkwi7c/_/n7ylpwh)

---

### r/LawFirm — 2026-01-25 | 8pts

> Beating up your attorneys won’t solve the issue.

My previous firm went through this. 

1) first they hired an “office manager” that brought big corp/big law style drama into our little firm.


That didn’t help matters at all and now the owner of this little 3 attorney firm is paying a full time position for someone whose only job is nag and harass attorneys about “their KPIs” and makes them waste time with a whole new layer of meetings and bureaucracy.

2) then he hired a “customer relationship manager”, in other words a 25 year old dude that picks up the phone and books meetings.

Did I mention that we also have a receptionist that picks up the phone and books meetings?  Did I mention both usually end passing the phone calls to the paralegals anyway? 

That’s another role/extra mouth to feed. 

3) then they began screeching about KPIs,case turnover and all that.  We have never had an issue with case turnover, we were a lean and mean firm! But now the “office manager” has to justify his job, and that means harassing the lawyers and paralegals. And now we have an “office manager” and a “CRM specialist” who are just overhead, so we gotta BILL BILL BILL!

4) so the firm’s owner decided it was time to cut costs… FINALLY! Ok, good, we will be back on track 🙂…. Wait, how is he going to cut costs? By doing the same greedy little thing you suggested, he fired an attorney and one parelegal so he could hire 3 “virtual paralegals” based in India and Philippines and a “foreign attorney” from India who does the stuff and sends it to the other attorneys to review because he can’t really do the attorney job without a US license, so now there is even more stuff on the (real) attorney’s plate, who are already getting choked by the ridiculous KPIs and harassment they’re subject to because they have to pay for the overhead cause by the office manager and the CRM guy.

Guess how the firm is doing now? Hint; I got the heck out of there because it’s a sinking ship. They were just fine from a profitability perspective and from a legal quality perspective until these “amazing optimizations” and “improvements in efficiency” were implemented.

Last I heard this firm is not worried about their rapidly declining profitability because “they will use AI to improve efficiency”, so I guess they are firing a paralegal or two, maybe even an attorney, “ai and smart forms will do it all”.

*— u/ZephyrPolar6* | [comment](https://reddit.com/r/LawFirm/comments/1qmbs7x/_/o1mh9ls)

---

### r/LawFirm — 2026-01-09 | 20pts

> Background: General practice solo (rep a ton of businesses, ep, probate, have some govt apppointments as a municipal public defender) in a small town.

I was also a true solo up until a 1.5 ish years ago. To put it shortly I combined a mix of 1 real human employee AND 1 human remote help (after using a phone answering service).

1. I had virtual hq as my call forwarding/phone answering service for a while. They were cost effective (almost too cost effective) and did a so-so job (they missed 1 out of every 5 calls), clients never get the same “receptionist” answering, and I got the feel that existing clients calling the office to speak quickly with me got grumpy when they were met with the answering service. With that said, they were a great, cheap and easy enough to use service, for about a year, when I wasn’t ready to hire anyone (but when I NEEDED some help). Using them allowed me to get my bearings on how to return calls, the flow of not having to rush to return calls when I personally missed them, etc. Without a doubt do not regret using them 1 iota;

2. Using virtual hq got me even busier. So busy I realized I needed someone to filter out the calls, refer out, and accordingly schedule (as you insinuated). I did double midnight moonless ninja recon on using a virtual paralegal………and opted against it. I came to the conclusion that if I was going to hire a remote paralegal for X amount of $ already, I’d rather spend a touch more and get a part time, in office, human being; which is exactly what I did. I hired a part time (2-3 days a week) woman who is responsible for calling clients, pc’s, talking to the court and scheduling. Absolute life changer (and in hindsight I have no idea how I would have ever been able to deal with a remote paralegal).  I offered as much hourly as I could afford ($19), told her I’m not meat, I continue to try and bonus her out a couple hundred bucks every month (I know it’s not a lot, but I’m doing my best) and generally try to make her life happy. I truly love her and she’s a part of my life now. 10/10

***Extra bonus: she thinks I’m too skinny and brings in donuts. 

****Also extra bonus: speaking from one solo to another, having another warm blooded person in the office a couple days a week really makes me feel like a grown up. Lol. It also motivates me (I’m assuming because it adds seriousness to the gig; I’ll talk to my therapist about it and report back though).

3. Hiring my office manager/secretary/paralegal/donut bringer-inner/yeller/line maintainer, made me even MORE busy. So busy it gave me stress; so busy that attorneys loved me for how much biz I was referring them. At this point in this overly long anecdote, I was still using virtual hq to handle calls for the days my office manager, Maria, was not in the office. I really tried to continue to use them, but it just wasn’t feasible anymore. I had too many current clients calling on a daily basis, too many attorneys trying to talk to me, and just generally t

*— u/bwalcott2* | [comment](https://reddit.com/r/LawFirm/comments/1q7jhqv/_/nyi4b5i)

---

### r/LawFirm — 2024-11-10 | 6pts

> I use my case
I’ve never even heard of the program that you use, but I’m going to check it out. I’m happy with mycase, but it can’t hurt to see what you’re using. 

I think you’re in estate planning. If so, you should reach out to divorce lawyers in the area that you service. Explain to them that once their clients are divorced they’ll need a new estate plan. (obviously you have to focus on the divorce lawyers that service the middle-class and upper class.) offer them a referral fee. I imagine you’ll get a fair amount of work.

I’m curious as to why you need Lexis. I’m not throwing any shade. I mean it’s an honest question. Estate planning law changes slowly. I run a family law firm 82.7% of our time is spent on Paternity, Divorce, and family law post judgment order modification. The rest is spent doing estate planning for our middle and upper class clients post judgment. 

I read what used to be called the advanced sheets— that is the appellate cases and state Supreme Court cases relevant to family law as they come out. They are free and I’m sure they’re free in your state too. On September 1, 2024 my state, California, modified the algebra equation we use to calculate child support. Legal news reported it six months before it happened so no surprises for us.

Depending on how much you’re earning the 350 you’re gonna be paying for Lexus could be significant and might be a cost you can do without

I found that if you focus on a certain area such as estate planning or family law, the amount of new laws very modest and as a result, Alexis or West law subscription is unnecessary  (using fastlaw) to ensure any cases you cite are up-to-date (ie Shepardize the cases).

I’m very interested in your virtual legal assistant. And I’d love it if you had the time too expand on that either on this post or DM. I have four experience, legal assistance and office manager one real receptionist +4 virtual receptionists that we pay for as an expense words I don’t give them 1099s. 

I love my virtual receptionists. I’ve made an effort to get to know them and to be interested in them at least superficially and they really do a great job for us. The way we have it set up. Is potential clients go to me or to the office manager. and we can switch that up on the fly. My unique sales proposition is that I have a lot of litigation experience,  so I’m in court three days out of five. But I don’t always have to spend the entire day there. Plus our court takes a lunch break from 12 to 130 during which I spent a portion of my time prepping the parties and witnesses for the second half of the day and a portion of my time returning calls.

I think it’s important that the owner of the firm takes client calls often.   I’m personable. I speak plainly and I am the person who is best able to judge whether the client is a good fit.

*— u/newdaynewrule* | [comment](https://reddit.com/r/LawFirm/comments/1gnu0ga/_/lwefhdt)

---

### r/LawFirm — 2025-12-29 | 0pts

> Thanks for posting these stats - very helpful as a real world example to those that are microbusinesses. 

I've been using a service called Apex chat (now called Blazeo) for many years on my website as a marketing agency owner (you can go to my site to try out the chat). They recently launched a very affordable phone-answering service with either fully AI or human receptionists. Their minimum package is a few hundred a month and it's totally worth it!

Like my marketing agency, they also specialize in medical and legal among other businesses. I highly recommend checking them out! Happy to also introduce you to my rep, David.

*— u/bluehuki* | [comment](https://reddit.com/r/LawFirm/comments/1py4kva/_/nwhvs1k)

---

### r/SaaS — 2025-05-24 | 1pts | Mentions: **Smith.ai, Dialzara**

**Looking for the best AI receptionist. Tried Sonant so far, curious what others are using**

> Looking for the best AI receptionist. Tried Sonant so far, curious what others are using

I’ve been exploring AI receptionists to help handle incoming calls and reduce missed opportunities for my small insurance office. Most of my callers hang up without leaving a voicemail, and it’s been a recurring issue during busy hours. 

I recently started using Sonant AI and it’s been a game changer. It answers instantly 24/7, and handles basic stuff like intake questions and appointment requests without missing a beat. And it sounds real and most people have no idea that it’s AI. It also integrates easily with the systems I already use which is just great.

That said, there are a ton of options out there like Smith AI, Dialzara, etc. but their pricing and features are all over the place. Has anyone done a deep dive or tested multiple tools? Curious what’s actually worked well for others in practice.

*— u/realsaqibmalik* | [post](https://reddit.com/r/SaaS/comments/1ku5d0n/looking_for_the_best_ai_receptionist_tried_sonant/)

---

### r/agency — 2023-10-20 | 0pts

> Hi, would highly recommend only going with setting up a general agency. I don't think this means just trying to do everything, but as an agency, you should be able to do all the websites that you have mentioned here.

So what you can do is, start as a general agency, **then with SEO**, have pages for each niche that you have mentioned here. For example, have your main website, then have /pages section and then /pages/lawyer-websites, this can be a template, that shows your process, the websites that you have built, the testimonials - and target all the keywords you want.

You can also do this with content, you can put content targeting all these keywords that you mentioned and then you will be providing a service to them. 

As an agency, you will be sending out contracts, constantly changing them to fit each client, with our product you can Get lawyer-level legal documents and revisions with our best-in-class AI: [Airstrip AI](https://useairstrip.com). If you want a document for a new client, you can tell our AI what to change, with the new terms, and you will get a new version of the document with those automatically made changes.

The documents have been tested and they are high quality, but if it doesn't provide accurate results based on your inputs, we can provide a full refund. Hope this answers your question!

*— u/ShanjaiRaj* | [comment](https://reddit.com/r/agency/comments/17bxlcs/_/k5ob9x8)

---

### r/agency — 2025-01-16 | 3pts

> 1/2

First things first you have to ask yourself - why would someone buy a website from you? When they ask what you do that’s better, what are you gonna say? When they ask about SEO and ranking better and what you do for that, what are you gonna say? What problems are you solving for them? What is wrong with their current site, why is it wrong, how do you fix it, and why are you uniquely able to fix it? Sales is the first Hurdle for most developers. It’s not easy. It’s a whole other way of thinking and now you have to talk to people, be personable, knowledgeable, and navigate the conversation skillfully to close the sale. It’s not about the website or their old one looking bad. It’s about what problems you solve. People buy solutions. And if you don’t have any, you won’t sell very much. So you need to work on that. What is your unique selling point, what do you do better than anyone else, and what problems you are solving for them and why it’s a problem. And if all you’re doing is slinging cheap crappy Wordpress themes then you are no better than Raj in Pakistan charging $200 on fiver. You can’t compete and you won’t solve any problems, which means you won’t get referrals or repeat business because your websites just sit there like their old ones did. It looks better. But they have no traffic and no conversions. Why? If you can’t answer that question then you aren’t ready to start.

Also Focus on how to use flexbox and grid, transforms, transitions, mobile first coding, positioning, differences between display block and Inline block, etc. very important to have the basics mastered.

I HIGHLY recommend finding a good designer to work with. You can find good ones for $20 an hour in Asia, Bangladesh, and Indonesia. They’re amazing out there. My guy in Bangladesh is the core of my design team. I gave him a raise to $25 an hour. And once we keep growing I’m bumping that up too and taking care of them nicely. Design is hard. I try to do it myself sometimes, but it’s always just easier having someone better at it than you so you can focus on the things you do better and are more productive at. You’ll be glad you did.

Then there’s pricing!

I have two packages:

I have lump sum $3800 minimum for 5 pages and $25 a month hosting and general maintenance

or $0 down $175 a month, unlimited edits, 24/7 support, hosting, etc.

$100 one time fee per page after 5, blog integration $250 for a custom blog that you can edit yourself.

Lump sum can add on the unlimited edits and support for $50 a month + hosting, so $75 a month for hosting and unlimited edits.

Nice, simple pricing. Simple projects. No databases. No booking features. No payment processing. Wanna know why? Because you don’t have to build everything yourself. There’s so many third party services out there that do niche specific booking services and perfected it for you. Just have your client set up a few demos with some companies and find the one that works best for them, their company rep will help 

*— u/Citrous_Oyster* | [comment](https://reddit.com/r/agency/comments/1i2op4n/_/m7hu3po)

---

### r/LawFirm — 2024-04-06 | 2pts | Mentions: **Smith.ai**

> I’m not a lawyer, I’m a growth strategist  and fractional CMO for lawyers/ firms and you’re getting amazing advice here. 

A few things I’d add: 

1. Wordpress website all the way. Make sure whoever builds it sets it up with good SEO and meta data for google to crawl.
2. Make sure there’s a way to connect or call you off the website. And ensure you have voicemail or get a service like Smith.ai to help.
3. PPC ads are a great start getting regular traffic to your website. If you have more than once practice area, create a campaign that goes to that practice area page in your site. 
4. Set up your google my business profile and keep it relevant.  Ask past clients for reviews google or set up an Alphafox account and connect it to fb and gmb.
5. Use HubSpot or Clio Grow and set up (or pay someone) to set up automations and tasks to remind you to follow up or send a reminder etc 
6. Yo already know you need to network so make that a priority 
7 Use LinkedIn to grow your online network and spend 10-15 min a day building it 

Once you’ve got some clients going and you want more or you’ve hired on a few paralegals or a few more attorneys then there’s advanced marketing strategies I’d recommend that will attract 10-30 new potential leads a day. 

I’m excited for you. I hope it goes well! 

If you’re got more questions feel free to ask.

*— u/blocdebranche* | [comment](https://reddit.com/r/LawFirm/comments/1bx1nwl/_/kydkwn7)

---

### r/LawFirm — 2026-01-08 | 1pts

> Hello! I know this post is years old at this point, but I noticed that no one actually answered the question. So for you, and anyone else who is curious -- yes, The Advocates and Targeted Legal Staffing Solutions are both very legitimate companies! They have the same address, list the same processes and have similar website copy because they were both founded by the same person who is currently president/CEO of both. The difference is that The Advocates works with exclusively lawyers, associates and partners, whereas Targeted Legal works with support staff and contract workers/temps (paralegals, legal assistants, office managers, and attorneys doing contract based work). There are various employees (like marketing, HR and admin) that work on both sides of the sister firms, but each company has a separate team of recruiters that are familiar with the specific market they are recruiting for. The Advocates has been around for over 20 years and has been Forbes ranked multiple times, and they work directly with many AmLaw 100 firms, hence the early access to opportunities, due to their relationship with various firms they also have the ability to directly present candidates to firms even if the firm may not be actively hiring or have any open job postings. I have worked with them in the past and they were very thoughtful, kind and professional and it felt different from working with any recruiter I've ever met in the past. If you are a law firm or working in the legal field, I highly recommend checking out their services!

*— u/literary_princess* | [comment](https://reddit.com/r/LawFirm/comments/74tm2g/_/nyfr6yg)

---

### r/LawFirm — 2025-12-09 | 1pts

> I have a pretty sizable PI firm and went the route of building a call center in-house. Man was that a headache and also very pricey.

Highly recommend just us⁤ing an answering service that specializes in law firms. Don't use a generic one that answers for tons of industries.

It's the difference between a significant amount of heavy lifting setting up a call center vs snapping your fingers and having people answering the phone professionally in a day.

Not to mention it's less than 1/10 of the cost. I found this company called Inside Out Law Calls last year, and I've been working with them since.

*— u/0rtmo* | [comment](https://reddit.com/r/LawFirm/comments/18076y4/_/nt3399v)

---

### r/LawFirm — 2025-07-17 | 15pts

> If a potential client calls and they get a voicemail, they may just call the next lawyer. 

Generally if I’m trying to get an appointment with any service, unless that service was specifically and highly recommended to me, I will call around until I have an appointment that’s convenient for me. This is true of most people, and thus you want someone real answering the phones 24/7 if you’re in a consumer-facing practice area.

*— u/lametowns* | [comment](https://reddit.com/r/LawFirm/comments/1m1nj30/_/n3ks2gs)

---

### r/LawFirm — 2025-06-21 | 1pts

> My firm uses an answering service. We like it because it gives us an idea of what the lead is so we can make a determination if the lead is bs or something we can actually help out with. I highly recommend it

*— u/zackalack7* | [comment](https://reddit.com/r/LawFirm/comments/1lgkrpj/_/myzf7h2)

---

### r/LawFirm — 2025-03-29 | 1pts

> With a single ad in a local directory and some worthwhile people referring or in your corner, you'll be just fine. Lawyers are always in demand, and the best ones are always  the ones with a life.

Dont get cornered into the perception of what a lawyer is expected to suffer thru with this or that person or firm. There are 12 lawyers in my family, and all worked for three years max before going solo practice. Solo practice means a hit some months with the rental space costs and if you need notary services etc, but a great- vetted- tactfully chosen- secretary means the time is wittled down significantly.

 If budgeting for reduced income at first, I highly recommend (at least for consults and contracts) time slots at office buildings instead of entire office rentals when meeting with clients. Depending on your law specialty, it can be awesome to be a solo lawyer- and the key in many places is your people. Your tech guy-  client info and seamless website, which is easily used on any device, and is set up to not allow junkmail. Internet reputation.

Answering service and proficient/ experienced secretary that can truly lighten the load with intake, and proper investment in software to automate many forms with template banks and support. 

Otherwise, work is easier when you get enough sleep and don't resent the hours spent watching your kids grow up at weekly dinners that are often spent half mentally dead from stress.

*— u/RageIntelligently101* | [comment](https://reddit.com/r/LawFirm/comments/1jmeu0x/_/mkbu1d7)

---

### r/LawFirm — 2024-11-28 | 1pts

> Hi there

I am the owner of LexScaleUp, a digital marketing agency specialized in helping law firms, so I can provide a bit of perspective on this.

The short answer is yes: SEO, search and social media advertising can help a wills and estate practice grow.

Let me explain why:   
  
From a marketing point of view you have two types of actions:  
1/ Demand capture actions, which aim to capture existing demand for legal services (people who are actively looking for an estate law firm)  
2/ Demand generation actions, which aim to generate demand for legal services (people who are not specifically looking for a solution right now, but they could be interested)

The content you will deploy to capture demand will be different than the one you'll use to generate demand. And not all channels are good at both capture and generation. 

Search (SEO and ads) is one of the channels that works great on both side of the equation (which is why Google is so valuable as a business):   
\- You can capture existing demand by targeting search terms like "will solicitor near me", "estate attorney near me", "best will law firm in \[location\]", etc.   
\- You can generate demand by targeting search terms like: "what does getting your affairs in order mean?", "when should one plan for end of life?", "Is it worth writing a will in 202\[5\]?"

Social media advertising is also good at both, though it is better at generating demand than capturing it. This is because you don't go on Instagram to look for a solicitor, you go to see updates from your friends, memes. You might stumble upon an ad about a will solicitor just as you were thinking about getting yours done, but that's not why you went on social initially. 

So typically, the way you would use social media is as follows:   
\- You would run a demand generation campaign: for example an ad saying "Have you got your affairs in order? Discover the 10 steps 40+ years old should take to avoid family disputes after their passing." (that's just an example). Now, people who click on this ad could be interested in getting their will done, we've generated the demand!  
\- Then, the next step would be to capture the demand we've just generated. For this, you would retarget everybody who engaged with the previous ad with a demand capture ad, for example: "10% off will writing at [Example.com](http://Example.com), get your affairs in order today!".    
\- And then we would layer another retargeting campaign on top, targeting everybody who has been on your website and hasn't converted into a lead/client with case studies and other brand focused content aimed at helping them choose your law firm: "Highly recommend [Example.com](http://Example.com), I used them to write my will, now I have peace of mind knowing that my affairs are in order - John Doe"  
  
That's a very simplistic example, but you get the idea: on one hand we capture demand from people actively looking for our solutions, and on the other we plant the seeds (like in 

*— u/lexscaleup-guillaume* | [comment](https://reddit.com/r/LawFirm/comments/1ge6w4f/_/lzfp5hi)

---

### r/LawFirm — 2024-11-18 | 1pts

> While I was in law school, I actually used to work for an answering service for money on the side. The business name is Keystone Answering Service. I would highly recommend them! They’re very professional and most of their employees are career answering service operators. Feel free to DM me if you have any questions!

*— u/CardiologistBorn1339* | [comment](https://reddit.com/r/LawFirm/comments/1guadrz/_/lxtyejl)

---

### r/LawFirm — 2024-05-27 | 1pts

> Hey, I was just wondering if 1) anyone can make a rec for an answering service they have succeeded with and 2) how well this worked with a Google ad campaign. I've used a few services and am not happy with them. Any feedback is greatly appreciated. Thanks.

I highly recommend VMeDx for your virtual receptionist needs. Their virtual receptionist services have been outstanding for our practice, providing professional and efficient handling of all patient queries.

VMeDx has proven to be highly effective in integrating with a Google ad campaign. When we started using their service in conjunction with our Google ads, we noticed a significant increase in conversion rates. The virtual receptionists are quick to respond and knowledgeable, helping capture leads effectively. I highly recommend giving them a try! So far, our experience with VMeDx's virtual receptionist and Google ad combination has been excellent. Their team is skilled in managing both aspects seamlessly, allowing us to focus on other important tasks while still gaining new patients through our ads. VMeDx offers the best virtual receptionist and Google ad package, providing exceptional value for any medical practice. [So, if you're looking for a reliable and successful virtual receptionist and Google ad solution, I highly recommend trying VMeDx. Their expertise and experience can take your practice to the next level. Don't hesitate to contact them and see the difference it makes in your patient acquisition process. ](https://vmedx.com/virtual-receptionist/)

*— u/xnormaltr4565* | [comment](https://reddit.com/r/LawFirm/comments/183yb9d/_/l5uy62h)

---

### r/agency — 2025-09-04 | 5pts

> It's obviously hard for me to tell if it's possible but you need to look at automating these kinds of processes.
I'd imagine that these mock ups can definitely be created by AI, maybe a little less perfect than you can make them right now but at a much higher frequency.

I obviously work on automations like that but I actually believe in the product. When you say you reached out to 23 people that really isn't a lot.
Quantity isn't always the answer but in this case you can see that there are gonna be a lot of clients that aren't even looking for the service you are offering.
Spending several hours on these proposals therefore is a big waste of time because the process isn't replicable.

I highly recommend you to implement an Automation and focus on the quality of the AIs output by refining it instead of doing this process over and over again yourself.

*— u/TomAutomates* | [comment](https://reddit.com/r/agency/comments/1n817pt/_/nccpd61)

---

### r/agency — 2023-09-22 | 2pts

> Hey! Just wanted to say that the agency model is very hard. Don't get discouraged and keep trying new things. Here are some ideas that can potentially help you out:

1. I would like to begin this list by mentioning an important point. When you start a service-based business, it typically means that you have mastered a craft and have reached a stage where you can provide real value to other people who are looking for that skill. In the beginning, I recommend solely focusing on the abilities that make YOU unique. For example, in my own case, I started helping people with designing their websites even though my main true skill was software engineering. This was really because I was prioritizing immediate cash flow rather than a long-term vision. 
2. Once you have niched down your services, it's now time to figure out who your ideal customers are. I will be writing a detailed post on how I did this for my consulting business but here's a quick summary:
   1. Reverse engineer your customer.
   2. Assume that you are someone who has recently purchased your services and answer the following questions: who am I? when did I buy? why did I buy? what exactly did I buy?
   3. Go into as much detail when answering these questions. You will thank me later.
   4. After doing so, you will be able to see a few potential avatars for your business. Pick the one that feels the best to you and whom you're confident servicing. 
3. Once you have determined your ICP, it's time to implement your marketing channels. This will be highly custom for your business so I won't go into exact details but there are typically 4 main avenues of customer acquisition:
   1. Warm outreach: message people that you know. start an actual conversation. ask them if they know anyone who is interested in your services. DO NOT ask them if they want to buy.
   2. Cold outreach: message people that you don't know. I recommend looking into [instantly.ai](https://instantly.ai). Their free training program is amazing for this.
   3. Content: This is what I'm personally spending a lot of time on these days. creating an online brand is definitely worth the effort. Give without asking and you will reap the rewards.
   4. Paid ads: Google Ads. Meta Ads, etc. I also recommend going with more niche avenues. For example, if you are building a product and have the budget, pay IndieHackers to feature them in their weekly newsletter!
4. Some bonus channels:
   1. Referrals: message your previous customers and ask who in their contacts is a great potential customer (like them) for your services. You can further increase the chance of closing this lead by providing a personalized coupon with an expiration.
   2. Partner with other agencies and affiliates. For example, if you offer web design services, team up with marketing agencies!

Hope this helps!

Parsa

*— u/_parsat* | [comment](https://reddit.com/r/agency/comments/16pj8ga/_/k1s586r)

---

### r/agency — 2023-03-27 | 5pts

> We do have a set process for onboarding of all new staff. 

In their first week, we cover topics like:
* Agency Induction - what our agency is, our values, org structure, products, services, process, position, ideal client, etc. 
* Agency strategy - what the agency is currently aiming to achieve in the current financial year and our medium term vision. 
* Department &amp; job induction - for each new employee to know what their departments structure, capabilities, and responsibilities are 
* HR induction - to cover the agency benefits, leave policy/process, pay, training, team principles, etc. 

The above is done either via confluence (documentation and guides); presentation decks (agency strategy/vision); and PDF handbooks (team/department guides and HR)

Separately we select a “buddy” to pair with the new hire. The buddy is ideally a medium to long term standing staff who can help the new hire (aside from the hire’s immediate manager) for any support or guidance. 

We use BambooHR to help build a checklist of all the things a new employee needs to have/know - and it automatically assigns a bunch of tasks to the manager, buddy, HR, IT etc. 

If they are going to be assigned to an existing platform/project, then they are given time to review all the notes, guides, and documentation about that project. For larger projects of clients we have had for a number of years, we have built a little quiz (10-20 questions) that they have to answer after they’ve read about the platform. 

In a similar vein, we also have off boarding processes (also managed in BambooHR) to collect feedback, turn off access, etc. when someone leaves. 

After 2-3 weeks of starting, each new hire fills a feedback form to assess their onboarding experience with the agency. We found that hires who rated the onboarding experience more positively, performed better and stayed with the agency longer. So for us, it’s a crucial step. 

The above is primarily done for full time staff - rather than contractors (though for contractors they do review the project docs and any associated quizzes for their assigned work). 

Apologies that I can’t share any specific examples, as a lot of it is IP we’ve created about our agency and strategic vision which is intertwined in our write ups. It gets reviewed each year. 

Hope it helps, and I can highly recommend building your onboarding process out as I it directly relates to staff retention. But don’t forget to continually iterate your onboarding processes based on staff feedback. Good luck!

*— u/agency-gm* | [comment](https://reddit.com/r/agency/comments/123njag/_/jdx5iet)

---

### r/LawFirm — 2024-05-24 | 1pts

> # Best virtual receptionist/google ads

# I'm sharing my experience with VMeDx as a virtual receptionist service. I've found it incredibly reliable, especially compared to other services I've tried. Not only do they handle calls professionally, but their integration with my Google ad campaign has been seamless. This combination has significantly boosted my customer engagement and overall satisfaction. I highly recommend VMeDx to anyone looking for a top-notch virtual receptionist and a successful Google ad campaign. Overall, I have seen great success using VMeDx as my virtual receptionist and incorporating their services into my Google ad campaign. It has dramatically improved my customer satisfaction and increased engagement, making it the best option. Try VMeDx to enhance their virtual receptionist services and Google ad campaign. Your customers will thank you! So, in my personal experience, using VMeDx as a virtual receptionist paired with a successful Google ad campaign has been the most effective and efficient way to handle customer calls and boost engagement.

*— u/xnormaltr4565* | [comment](https://reddit.com/r/LawFirm/comments/183yb9d/_/l5ftcsj)

---

### r/LawFirm — 2024-04-13 | 1pts

> Absolutely, going for a virtual receptionist, especially when you're starting out, is a smart choice. We've been using VMeDx for our medical practice's virtual receptionist needs, and it's been a game-changer. Not only do they handle calls in both English and Spanish, which is crucial for our diverse client base, but they also offer a wide array of services that extend beyond traditional reception duties. The cost varies depending on the package you choose, but their flexibility and efficiency are well worth the investment. Definitely worth checking out their website for more detailed information on pricing and services!  So, don't hesitate to consider a virtual receptionist for your law firm as it can greatly benefit your business in terms of cost-effectiveness and convenience. [VMeDx has been a reliable partner for us, and we highly recommend their services.](https://vmedx.com/virtual-receptionist/)

*— u/dubliuno* | [comment](https://reddit.com/r/LawFirm/comments/190sf6s/_/kzdeuqk)

---

### r/consulting — 2023-01-03 | 13pts

> This process will vary by firm. While we could suggest some generic trainings, your firm’s requirements for margin, process to estimate, how the interplay and approvals are done across service lines, etc. will vary by firm. Unfortunately. 

General process will be —

1. Prospective client issues a Request for Proposal (RFP) 

2. A sales team is put together with folks from each service line, each service line solutions and prices to meet the client’s request, with daily calls occurring across service line to share updates 

3. A solution review is done (by service line and firm leadership)

4. Proposal content is compiled, usually not drafted from scratch but leveraging similar past proposals, stitching together, and customizing, including verbiage and graphics 

5. Reviews are done on the proposal content (by service line and firm leadership)

6. Costs are estimated by service line, then looked at overall in a deal review (by service line and firm leadership) 

7. After proposal is submitted, client will down-select a few vendors to participate in orals. Each service line will provide representation. An orals deck will be compiled and dress rehearsals with all presenters 

8. If team wins, a statement of work will be drafted, with each service line drafting its portion, and going through all necessary approvals with firm leadership, finance, legal, client review, etc. and there will be next steps to contract, staff, onboard, which is where it hands off from the sales team to the delivery team 

Proposals are weird. You can do a little work on a proposal with high dollar value, win it, and your sales numbers look great. Or a lot of work on a bunch of little proposals, or non-winning proposals, that yields the same or lesser outcome. Start wherever they’ll let you to get your foot in the door and learn. Stick on the daily calls. Observe. Help where you can. I personally love it when the juniors on my team cover the daily call as representatives for our service line. Save me 30 min of my day, they learn, they bring back updates, and if they are asked something and do not know the answer, they can take it as an action to find out or ping me to join- it’s all internal so it’s ok to not have all the answers. I am professionally grateful for juniors who want to get involved like this!

*— u/Old_Scientist_4014* | [comment](https://reddit.com/r/consulting/comments/101kypo/_/j2qlx9k)

---

### r/LawFirm — 2023-03-24 | 7pts

> The easiest and best thing to do if you feel underpaid is to apply to other jobs and cultivate other opportunities. If they are offering more, then you can take an offer from one of them to your current employer and ask for an increase. If your current employer will not increase, then go work elsewhere. 

There is no right or wrong salary amount.  Employers generally will pay people what they are willing to accept for the work being performed. If an employer hires a receptionist that the employer thinks is incredible, and the receptionist only ask to be paid $10 an hour, it is not the responsibility of the employer to say, “No no no, I much prefer to pay you much higher than you are asking for.”

That’s not saying an employer shouldn’t pay more for great employees. If employers don’t want great employees even to consider going elsewhere, employers can stay on top of what competitors are paying and just match that without the employees even asking. 

So basically, develop your worth as an employee, and if you want to know what others would pay you, cultivate other opportunities and find out. Plus, asking for a raise without having a backup option is never a good idea.

*— u/FreudianYipYip* | [comment](https://reddit.com/r/LawFirm/comments/120sdjt/_/jdj2m92)

---

