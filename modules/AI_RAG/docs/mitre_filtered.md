# MITRE ATT&CK Mobile - 필터링된 큐싱/모바일 위협 인텔

### [CAMPAIGN] Operation Dust Storm
- relevance: medium (matched: korea)
- url: https://attack.mitre.org/campaigns/C0016

- **별칭**: Operation Dust Storm
- **설명**:
[Operation Dust Storm](https://attack.mitre.org/campaigns/C0016) was a long-standing persistent cyber espionage campaign that targeted multiple industries in Japan, South Korea, the United States, Europe, and several Southeast Asian countries. By 2015, the [Operation Dust Storm](https://attack.mitre.org/campaigns/C0016) threat actors shifted from government and defense-related intelligence targets to Japanese companies or Japanese subdivisions of larger foreign organizations supporting Japan's critical infrastructure, including electricity generation, oil and natural gas, finance, transportation, and construction.(Citation: Cylance Dust Storm)

[Operation Dust Storm](https://attack.mitre.org/campaigns/C0016) threat actors also began to use Android backdoors in their operations by 2015, with all identified victims at the time residing in Japan or South Korea.(Citation: Cylance Dust Storm)

---

### [CAMPAIGN] C0033
- relevance: low
- url: https://attack.mitre.org/campaigns/C0033

- **별칭**: C0033
- **설명**:
[C0033](https://attack.mitre.org/campaigns/C0033) was a [PROMETHIUM](https://attack.mitre.org/groups/G0056) campaign during which they used [StrongPity](https://attack.mitre.org/software/S0491) to target Android users. [C0033](https://attack.mitre.org/campaigns/C0033) was the first publicly documented mobile campaign for [PROMETHIUM](https://attack.mitre.org/groups/G0056), who previously used Windows-based techniques.(Citation: welivesec_strongpity)

---

### [CAMPAIGN] Operation Triangulation
- relevance: low
- url: https://attack.mitre.org/campaigns/C0054

- **별칭**: Operation Triangulation
- **설명**:
[Operation Triangulation](https://attack.mitre.org/campaigns/C0054) is a mobile campaign targeting iOS devices.(Citation: SecureList OpTriangulation 01Jun2023) The unidentified actors used zero-click exploits in iMessage attachments to gain [Initial Access](https://attack.mitre.org/tactics/TA0027), then executed exploits and validators, such as [Binary Validator](https://attack.mitre.org/software/S1215) before finally executing the [TriangleDB](https://attack.mitre.org/software/S1216) implant.

---

### [COURSE-OF-ACTION] Use Recent OS Version
- relevance: low

- **설명**:
New mobile operating system versions bring not only patches against discovered vulnerabilities but also often bring security architecture improvements that provide resilience against potential vulnerabilities or weaknesses that have not yet been discovered. They may also bring improvements that block use of observed adversary techniques.

---

### [COURSE-OF-ACTION] Application Developer Guidance
- relevance: high (matched: credential, spoof)

- **설명**:
Application Developer Guidance focuses on providing developers with the knowledge, tools, and best practices needed to write secure code, reduce vulnerabilities, and implement secure design principles. By integrating security throughout the software development lifecycle (SDLC), this mitigation aims to prevent the introduction of exploitable weaknesses in applications, systems, and APIs. This mitigation can be implemented through the following measures:

Preventing SQL Injection (Secure Coding Practice):

- Implementation: Train developers to use parameterized queries or prepared statements instead of directly embedding user input into SQL queries.
- Use Case: A web application accepts user input to search a database. By sanitizing and validating user inputs, developers can prevent attackers from injecting malicious SQL commands.

Cross-Site Scripting (XSS) Mitigation:

- Implementation: Require developers to implement output encoding for all user-generated content displayed on a web page.
- Use Case: An e-commerce site allows users to leave product reviews. Properly encoding and escaping user inputs prevents malicious scripts from being executed in other users’ browsers.

Secure API Design:

- Implementation: Train developers to authenticate all API endpoints and avoid exposing sensitive information in API responses.
- Use Case: A mobile banking application uses APIs for account management. By enforcing token-based authentication for every API call, developers reduce the risk of unauthorized access.

Static Code Analysis in the Build Pipeline:

- Implementation: Incorporate tools into CI/CD pipelines to automatically scan for vulnerabilities during the build process.
- Use Case: A fintech company integrates static analysis tools to detect hardcoded credentials in their source code before deployment.

Threat Modeling in the Design Phase:

- Implementation: Use frameworks like STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) to assess threats during application design.
- Use Case: Before launching a customer portal, a SaaS company identifies potential abuse cases, such as session hijacking, and designs mitigations like secure session management.

**Tools for Implementation**:

- Static Code Analysis Tools: Use tools that can scan for known vulnerabilities in source code.
- Dynamic Application Security Testing (DAST): Use tools like Burp Suite or OWASP ZAP to simulate runtime attacks and identify vulnerabilities.
- Secure Frameworks: Recommend secure-by-default frameworks (e.g., Django for Python, Spring Security for Java) that enforce security best practices.

---

### [COURSE-OF-ACTION] Enterprise Policy
- relevance: low

- **설명**:
An enterprise mobility management (EMM), also known as mobile device management (MDM), system can be used to provision policies to mobile devices to control aspects of their allowed behavior.

---

### [COURSE-OF-ACTION] User Guidance
- relevance: low

- **설명**:
Describes any guidance or training given to users to set particular configuration settings or avoid specific potentially risky behaviors.

---

### [COURSE-OF-ACTION] Do Not Mitigate
- relevance: low

- **설명**:
This category is to associate techniques that mitigation might increase risk of compromise and therefore mitigation is not recommended.

---

### [COURSE-OF-ACTION] Antivirus/Antimalware
- relevance: low

- **설명**:
Mobile security products, such as Mobile Threat Defense (MTD), offer various device-based mitigations against certain behaviors.

---

### [COURSE-OF-ACTION] System Partition Integrity
- relevance: low

- **설명**:
Ensure that Android devices being used include and enable the Verified Boot capability, which cryptographically ensures the integrity of the system partition.

---

### [COURSE-OF-ACTION] Encrypt Network Traffic
- relevance: low

- **설명**:
Application developers should encrypt all of their application network traffic using the Transport Layer Security (TLS) protocol to ensure protection of sensitive data and deter network-based attacks. If desired, application developers could perform message-based encryption of data before passing it for TLS encryption.

iOS's App Transport Security feature can be used to help ensure that all application network traffic is appropriately protected. Apple intends to mandate use of App Transport Security  (Citation: TechCrunch-ATS) for all apps in the Apple App Store unless appropriate justification is given.

Android's Network Security Configuration feature similarly can be used by app developers to help ensure that all of their application network traffic is appropriately protected  (Citation: Android-NetworkSecurityConfig).

Use of Virtual Private Network (VPN) tunnels, e.g. using the IPsec protocol, can help mitigate some types of network attacks as well.

---

### [COURSE-OF-ACTION] Lock Bootloader
- relevance: low

- **설명**:
On devices that provide the capability to unlock the bootloader (hence allowing any operating system code to be flashed onto the device), perform periodic checks to ensure that the bootloader is locked.

---

### [COURSE-OF-ACTION] Security Updates
- relevance: low

- **설명**:
Install security updates in response to discovered vulnerabilities.

Purchase devices with a vendor and/or mobile carrier commitment to provide security updates in a prompt manner for a set period of time.

Decommission devices that will no longer receive security updates.

Limit or block access to enterprise resources from devices that have not installed recent security updates.

On Android devices, access can be controlled based on each device's security patch level. On iOS devices, access can be controlled based on the iOS version.

---

### [COURSE-OF-ACTION] Deploy Compromised Device Detection Method
- relevance: medium (matched: sms)

- **설명**:
A variety of methods exist that can be used to enable enterprises to identify compromised (e.g. rooted/jailbroken) devices, whether using security mechanisms built directly into the device, third-party mobile security applications, enterprise mobility management (EMM)/mobile device management (MDM) capabilities, or other methods. Some methods may be trivial to evade while others may be more sophisticated.

---

### [COURSE-OF-ACTION] Interconnection Filtering
- relevance: low

- **설명**:
In order to mitigate Signaling System 7 (SS7) exploitation, the Communications, Security, Reliability, and Interoperability Council (CSRIC) describes filtering interconnections between network operators to block inappropriate requests (Citation: CSRIC5-WG10-FinalReport).

---

### [COURSE-OF-ACTION] Attestation
- relevance: low

- **설명**:
Enable remote attestation capabilities when available (such as Android SafetyNet or Samsung Knox TIMA Attestation) and prohibit devices that fail the attestation from accessing enterprise resources.

---

### [INTRUSION-SET] Kimsuky
- relevance: high (matched: social engineering)
- url: https://attack.mitre.org/groups/G0094

- **별칭**: Kimsuky, Black Banshee, Velvet Chollima, Emerald Sleet, THALLIUM, APT43, TA427, Springtail, Earth Kumiho, PatheticSlug
- **설명**:
[Kimsuky](https://attack.mitre.org/groups/G0094) is a Democratic People's Republic of Korea (DPRK)-based cyber espionage group that has been active since at least 2012. The group initially targeted South Korean government agencies, think tanks, and subject-matter experts in various fields. Its operations expanded to include the United Nations and organizations in the government, education, business services, and manufacturing sectors across the United States, Japan, Russia, and Europe. [Kimsuky](https://attack.mitre.org/groups/G0094) has focused collection on foreign policy and national security issues tied to the Korean Peninsula, nuclear policy, and sanctions. [Kimsuky](https://attack.mitre.org/groups/G0094) operations have overlapped with those of other North Korean state-sponsored cyber espionage actors as a result of ad hoc collaborations or other limited resource sharing.(Citation: EST Kimsuky April 2019)(Citation: Cybereason Kimsuky November 2020)(Citation: Malwarebytes Kimsuky June 2021)(Citation: CISA AA20-301A Kimsuky)(Citation: Mandiant APT43 March 2024)(Citation: Proofpoint TA427 April 2024)

[Kimsuky](https://attack.mitre.org/groups/G0094) was assessed to be responsible for the 2014 Korea Hydro & Nuclear Power Co. compromise; other notable campaigns include Operation STOLEN PENCIL (2018), Operation Kabar Cobra (2019), and Operation Smoke Screen (2019).(Citation: Netscout Stolen Pencil Dec 2018)(Citation: EST Kimsuky SmokeScreen April 2019)(Citation: AhnLab Kimsuky Kabar Cobra Feb 2019) In 2023, [Kimsuky](https://attack.mitre.org/groups/G0094) was observed using commercial large language models (LLMs) to assist with vulnerability research, scripting, social engineering and reconnaissance.(Citation: MSFT-AI)

DPRK threat actor cluster boundaries overlap in open source reporting, with some security researchers consolidating all attributed North Korean state-sponsored cyber activity under [Lazarus Group](https://attack.mitre.org/groups/G0032), rather than tracking operationally distinct subgroups.

---

### [INTRUSION-SET] Patchwork
- relevance: high (matched: phishing, spearphishing)
- url: https://attack.mitre.org/groups/G0040

- **별칭**: Patchwork, Hangover Group, Dropping Elephant, Chinastrats, MONSOON, Operation Hangover
- **설명**:
[Patchwork](https://attack.mitre.org/groups/G0040) is a cyber espionage group that was first observed in December 2015. While the group has not been definitively attributed, circumstantial evidence suggests the group may be a pro-Indian or Indian entity. [Patchwork](https://attack.mitre.org/groups/G0040) has been seen targeting industries related to diplomatic and government agencies. Much of the code used by this group was copied and pasted from online forums. [Patchwork](https://attack.mitre.org/groups/G0040) was also seen operating spearphishing campaigns targeting U.S. think tank groups in March and April of 2018.(Citation: Cymmetria Patchwork) (Citation: Symantec Patchwork)(Citation: TrendMicro Patchwork Dec 2017)(Citation: Volexity Patchwork June 2018)

---

### [INTRUSION-SET] Scattered Spider
- relevance: high (matched: social engineering, impersonat)
- url: https://attack.mitre.org/groups/G1015

- **별칭**: Scattered Spider, Roasted 0ktapus, Octo Tempest, Storm-0875, UNC3944
- **설명**:
[Scattered Spider](https://attack.mitre.org/groups/G1015) is a native English-speaking cybercriminal group active since at least 2022. (Citation: CrowdStrike Scattered Spider Profile) (Citation: MSTIC Octo Tempest Operations October 2023) The group initially targeted customer relationship management (CRM) providers, business process outsourcing (BPO) firms, and telecommunications and technology companies before expanding in 2023 to gaming, hospitality, retail, managed service provider (MSP), manufacturing, and financial sectors. (Citation: MSTIC Octo Tempest Operations October 2023)
[Scattered Spider](https://attack.mitre.org/groups/G1015) relies heavily on social engineering, including impersonating IT and help-desk staff, to gain initial access, bypass multi-factor authentication (MFA), and compromise enterprise networks. The group has adapted its tooling to evade endpoint detection and response (EDR) defenses and used ransomware for financial gain. (Citation: CISA Scattered Spider Advisory November 2023) (Citation: CrowdStrike Scattered Spider BYOVD January 2023) (Citation: Crowdstrike TELCO BPO Campaign December 2022)
[Scattered Spider](https://attack.mitre.org/groups/G1015) had expanded into hybrid cloud and identity environments, using help-desk impersonation and MFA bypass to obtain administrator access in Okta, AWS, and Office 365. (Citation: Mandiant UNC3944 May 2025)

---

### [INTRUSION-SET] Star Blizzard
- relevance: high (matched: phishing, credential)
- url: https://attack.mitre.org/groups/G1033

- **별칭**: Star Blizzard, SEABORGIUM, Callisto Group, TA446, COLDRIVER
- **설명**:
[Star Blizzard](https://attack.mitre.org/groups/G1033) is a cyber espionage and influence group originating in Russia that has been active since at least 2019. [Star Blizzard](https://attack.mitre.org/groups/G1033) campaigns align closely with Russian state interests and have included persistent phishing and credential theft against academic, defense, government, NGO, and think tank organizations in NATO countries, particularly the US and the UK.(Citation: Microsoft Star Blizzard August 2022)(Citation: CISA Star Blizzard Advisory December 2023)(Citation: StarBlizzard)(Citation: Google TAG COLDRIVER January 2024)

---

### [INTRUSION-SET] LAPSUS$
- relevance: high (matched: social engineering)
- url: https://attack.mitre.org/groups/G1004

- **별칭**: LAPSUS$, DEV-0537, Strawberry Tempest
- **설명**:
[LAPSUS$](https://attack.mitre.org/groups/G1004) is cyber criminal threat group that has been active since at least mid-2021. [LAPSUS$](https://attack.mitre.org/groups/G1004) specializes in large-scale social engineering and extortion operations, including destructive attacks without the use of ransomware. The group has targeted organizations globally, including in the government, manufacturing, higher education, energy, healthcare, technology, telecommunications, and media sectors.(Citation: BBC LAPSUS Apr 2022)(Citation: MSTIC DEV-0537 Mar 2022)(Citation: UNIT 42 LAPSUS Mar 2022)

---

### [MALWARE] Cerberus
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S0480

- **설명**:
[Cerberus](https://attack.mitre.org/software/S0480) is a banking trojan whose usage can be rented on underground forums and marketplaces. Prior to being available to rent, the authors of [Cerberus](https://attack.mitre.org/software/S0480) claim was used in private operations for two years.(Citation: Threat Fabric Cerberus)

---

### [MALWARE] DroidJack
- relevance: medium (matched: remote access)
- url: https://attack.mitre.org/software/S0320

- **설명**:
[DroidJack](https://attack.mitre.org/software/S0320) is an Android remote access tool that has been observed posing as legitimate applications including the Super Mario Run and Pokemon GO games. (Citation: Zscaler-SuperMarioRun) (Citation: Proofpoint-Droidjack)

---

### [MALWARE] Rotexy
- relevance: medium (matched: banking, sms)
- url: https://attack.mitre.org/software/S0411

- **설명**:
[Rotexy](https://attack.mitre.org/software/S0411) is an Android banking malware that has evolved over several years. It was originally an SMS spyware Trojan first spotted in October 2014, and since then has evolved to contain more features, including ransomware functionality.(Citation: securelist rotexy 2018)

---

### [MALWARE] SpyNote RAT
- relevance: high (matched: malicious app)
- url: https://attack.mitre.org/software/S0305

- **설명**:
[SpyNote RAT](https://attack.mitre.org/software/S0305) (Remote Access Trojan) is a family of malicious Android apps. The [SpyNote RAT](https://attack.mitre.org/software/S0305) builder tool can be used to develop malicious apps with the malware's functionality. (Citation: Zscaler-SpyNote)

---

### [MALWARE] TrickMo
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S0427

- **설명**:
[TrickMo](https://attack.mitre.org/software/S0427) a 2FA bypass mobile banking trojan, most likely being distributed by [TrickBot](https://attack.mitre.org/software/S0266). [TrickMo](https://attack.mitre.org/software/S0427) has been primarily targeting users located in Germany.(Citation: SecurityIntelligence TrickMo)

[TrickMo](https://attack.mitre.org/software/S0427) is designed to steal transaction authorization numbers (TANs), which are typically used as one-time passwords.(Citation: SecurityIntelligence TrickMo)

---

### [MALWARE] AhRat
- relevance: medium (matched: remote access)
- url: https://attack.mitre.org/software/S1095

- **설명**:
[AhRat](https://attack.mitre.org/software/S1095) is an Android remote access tool based on the open-source AhMyth remote access tool. [AhRat](https://attack.mitre.org/software/S1095) initially spread in August 2022 on the Google Play Store via an update containing malicious code to the previously benign application, “iRecorder – Screen Recorder,” which itself was released in September 2021.(Citation: welivesecurity_ahrat_0523)

---

### [MALWARE] XLoader for Android
- relevance: high (matched: fake)
- url: https://attack.mitre.org/software/S0318

- **설명**:
[XLoader for Android](https://attack.mitre.org/software/S0318) is a malicious Android app first observed targeting Japan, Korea, China, Taiwan, and Hong Kong in 2018. It has more recently been observed targeting South Korean users as a pornography application.(Citation: TrendMicro-XLoader-FakeSpy)(Citation: TrendMicro-XLoader) It is tracked separately from the [XLoader for iOS](https://attack.mitre.org/software/S0490).

---

### [MALWARE] Trojan-SMS.AndroidOS.FakeInst.a
- relevance: high (matched: fake)
- url: https://attack.mitre.org/software/S0306

- **설명**:
[Trojan-SMS.AndroidOS.FakeInst.a](https://attack.mitre.org/software/S0306) is Android malware. (Citation: Kaspersky-MobileMalware)

---

### [MALWARE] XLoader for iOS
- relevance: high (matched: fake)
- url: https://attack.mitre.org/software/S0490

- **설명**:
[XLoader for iOS](https://attack.mitre.org/software/S0490) is a malicious iOS application that is capable of gathering system information.(Citation: TrendMicro-XLoader-FakeSpy) It is tracked separately from the [XLoader for Android](https://attack.mitre.org/software/S0318).

---

### [MALWARE] Chameleon
- relevance: medium (matched: banking, accessibility service)
- url: https://attack.mitre.org/software/S1083

- **설명**:
[Chameleon](https://attack.mitre.org/software/S1083) is an Android banking trojan that can leverage Android’s Accessibility Services to perform malicious activities. Believed to have been first active in January 2023, [Chameleon](https://attack.mitre.org/software/S1083) has been observed targeting users in Australia and Poland by masquerading as official applications. A new variant of [Chameleon](https://attack.mitre.org/software/S1083) has expanded its targets to include Android users in the United Kingdom and Italy.(Citation: cyble_chameleon_0423)(Citation: ThreatFabric_Chameleon_Dec2023)

---

### [MALWARE] Dendroid
- relevance: medium (matched: remote access)
- url: https://attack.mitre.org/software/S0301

- **설명**:
[Dendroid](https://attack.mitre.org/software/S0301) is an Android remote access tool (RAT) primarily targeting Western countries. The RAT was available for purchase for $300 and came bundled with a utility to inject the RAT into legitimate applications.(Citation: Lookout-Dendroid)

---

### [MALWARE] KeyRaider
- relevance: high (matched: credential)
- url: https://attack.mitre.org/software/S0288

- **설명**:
[KeyRaider](https://attack.mitre.org/software/S0288) is malware that steals Apple account credentials and other data from jailbroken iOS devices. It also has ransomware functionality. (Citation: Xiao-KeyRaider)

---

### [MALWARE] CherryBlos
- relevance: high (matched: credential)
- url: https://attack.mitre.org/software/S1225

- **설명**:
[CherryBlos](https://attack.mitre.org/software/S1225) is an Android malware that steals credentials and redirects cryptocurrency to adversary-controlled wallets. [CherryBlos](https://attack.mitre.org/software/S1225) was labelled Robot 999 in its first appearance in April 2023; since then, various aliases have been used, including GPTalk, Happy Miner, and SynthNet. The threat actors behind [CherryBlos](https://attack.mitre.org/software/S1225) uploaded the malware to different Google Play regions, such as Malaysia, Vietnam, Indonesia, Philippines, Uganda, and Mexico.(Citation: TrendMicro_CherryBlos_July2023)

---

### [MALWARE] DocSwap
- relevance: high (matched: phishing)
- url: https://attack.mitre.org/software/S9005

- **설명**:
[DocSwap](https://attack.mitre.org/software/S9005) is an Android malware first identified in 2025, and attributed to [Kimsuky](https://attack.mitre.org/groups/G0094). [DocSwap](https://attack.mitre.org/software/S9005)’s name is a combination of its Korean name “문서열람 인증 앱” (Document Viewing Authentication App) and a phishing page masquerading as CoinSwap at the C2 address. Based on [DocSwap](https://attack.mitre.org/software/S9005)’s name and Korean-language strings, [DocSwap](https://attack.mitre.org/software/S9005) potentially targets mobile device users in South Korea. Several variants of [DocSwap](https://attack.mitre.org/software/S9005) exist; one of the latest samples indicates that the adversary added a native decryption function that decrypts an internal APK.(Citation: EnkiWhiteHat_KimsukyDOCSWAP_Dec2025)(Citation: S2W_DocSwap_Mar2025)

---

### [MALWARE] Fakecalls
- relevance: high (matched: fake)
- url: https://attack.mitre.org/software/S1080

- **설명**:
[Fakecalls](https://attack.mitre.org/software/S1080) is an Android trojan, first detected in January 2021, that masquerades as South Korean banking apps. It has capabilities to intercept calls to banking institutions and even maintain realistic dialogues with the victim using pre-recorded audio snippets.(Citation: kaspersky_fakecalls_0422)

---

### [MALWARE] S.O.V.A.
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S1062

- **설명**:
[S.O.V.A.](https://attack.mitre.org/software/S1062) is an Android banking trojan that was first identified in August 2021 and has subsequently been found in a variety of applications, including banking, cryptocurrency wallet/exchange, and shopping apps. [S.O.V.A.](https://attack.mitre.org/software/S1062), which is Russian for "owl", contains features not commonly found in Android malware, such as session cookie theft.(Citation: threatfabric_sova_0921)(Citation: cleafy_sova_1122)

---

### [MALWARE] DualToy
- relevance: high (matched: malicious app, malicious application)
- url: https://attack.mitre.org/software/S0315

- **설명**:
[DualToy](https://attack.mitre.org/software/S0315) is Windows malware that installs malicious applications onto Android and iOS devices connected over USB. (Citation: PaloAlto-DualToy)

---

### [MALWARE] HilalRAT
- relevance: medium (matched: remote access)
- url: https://attack.mitre.org/software/S1128

- **설명**:
[HilalRAT](https://attack.mitre.org/software/S1128) is a remote access-capable Android malware, developed and used by [UNC788](https://attack.mitre.org/groups/G1029).(Citation: Meta Adversarial Threat Report 2022)   [HilalRAT](https://attack.mitre.org/software/S1128) is capable of collecting data, such as device location, call logs, etc., and is capable of executing actions, such as activating a device's camera and microphone.(Citation: Meta Adversarial Threat Report 2022)

---

### [MALWARE] DEFENSOR ID
- relevance: medium (matched: banking, accessibility service)
- url: https://attack.mitre.org/software/S0479

- **설명**:
[DEFENSOR ID](https://attack.mitre.org/software/S0479) is a banking trojan capable of clearing a victim’s bank account or cryptocurrency wallet and taking over email or social media accounts. [DEFENSOR ID](https://attack.mitre.org/software/S0479) performs the majority of its malicious functionality by abusing Android’s accessibility service.(Citation: ESET DEFENSOR ID)

---

### [MALWARE] BRATA
- relevance: medium (matched: remote access)
- url: https://attack.mitre.org/software/S1094

- **설명**:
[BRATA](https://attack.mitre.org/software/S1094) (Brazilian Remote Access Tool, Android), is an evolving Android malware strain, detected in late 2018 and again in late 2021. Originating in Brazil, [BRATA](https://attack.mitre.org/software/S1094) was later also found in the UK, Poland, Italy, Spain, and USA, where it is believed to have targeted financial institutions such as banks. There are currently three known variants of [BRATA](https://attack.mitre.org/software/S1094).(Citation: securelist_brata_0819)(Citation: cleafy_brata_0122)(Citation: mcafee_brata_0421)

---

### [MALWARE] LightSpy
- relevance: high (matched: credential)

- **설명**:
First observed in 2018, LightSpy is a modular malware family that initially targeted iOS devices in Southern Asia before expanding to Android and macOS platforms. It consists of a downloader, a main executable that manages network communications, and functionality-specific modules, typically implemented as `.dylib` files (iOS, macOS) or `.apk` files (Android). LightSpy can collect VoIP call recordings, SMS messages, and credential stores, which are then exfiltrated to a command and control (C2) server.(Citation: MelikovBlackBerry LightSpy 2024)

---

### [MALWARE] MazarBOT
- relevance: medium (matched: sms)
- url: https://attack.mitre.org/software/S0303

- **설명**:
[MazarBOT](https://attack.mitre.org/software/S0303) is Android malware that was distributed via SMS in Denmark in 2016. (Citation: Tripwire-MazarBOT)

---

### [MALWARE] Ginp
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S0423

- **설명**:
[Ginp](https://attack.mitre.org/software/S0423) is an Android banking trojan that has been used to target Spanish banks. Some of the code was taken directly from [Anubis](https://attack.mitre.org/software/S0422).(Citation: ThreatFabric Ginp)

---

### [MALWARE] TangleBot
- relevance: medium (matched: sms)
- url: https://attack.mitre.org/software/S1069

- **설명**:
[TangleBot](https://attack.mitre.org/software/S1069) is SMS malware that was initially observed in September 2021, primarily targeting mobile users in the United States and Canada. [TangleBot](https://attack.mitre.org/software/S1069) has used SMS text message lures about COVID-19 regulations and vaccines to trick mobile users into downloading the malware, similar to [FluBot](https://attack.mitre.org/software/S1067) Android malware campaigns.(Citation: cloudmark_tanglebot_0921)

---

### [MALWARE] RatMilad
- relevance: high (matched: fake)
- url: https://attack.mitre.org/software/S1241

- **설명**:
[RatMilad](https://attack.mitre.org/software/S1241) is an Android remote access tool (RAT) with spyware functionality that has been used to target enterprise mobile devices in the Middle East since at least 2021. Variants of [RatMilad](https://attack.mitre.org/software/S1241) have been disguised as VPN applications and a fake app named NumRent. Upon installation, [RatMilad](https://attack.mitre.org/software/S1241) employs multiple [Collection](https://attack.mitre.org/tactics/TA0035) techniques to collect sensitive information before uploading the collected data to its command and control (C2) server. (Citation: ZimperiumGupta_RatMilad_Oct2022)

---

### [MALWARE] DCHSpy
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S1243

- **설명**:
[DCHSpy](https://attack.mitre.org/software/S1243) is an Android spyware likely used by [MuddyWater](https://attack.mitre.org/groups/G0069). [DCHSpy](https://attack.mitre.org/software/S1243) uses political decoys and masquerades as legitimate applications, such as VPNs and banking applications, to trick victims into downloading the malware. Once downloaded, [DCHSpy](https://attack.mitre.org/software/S1243) collects information from the device and exfiltrates the data to the command and control (C2) server.(Citation: Lookout_DCHSpy_July2025)

---

### [MALWARE] Red Alert 2.0
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S0539

- **설명**:
[Red Alert 2.0](https://attack.mitre.org/software/S0539) is a banking trojan that masquerades as a VPN client.(Citation: Sophos Red Alert 2.0)

---

### [MALWARE] FlyTrap
- relevance: high (matched: social engineering)
- url: https://attack.mitre.org/software/S1093

- **설명**:
[FlyTrap](https://attack.mitre.org/software/S1093) is an Android trojan, first detected in March 2021, that uses social engineering tactics to compromise Facebook accounts. [FlyTrap](https://attack.mitre.org/software/S1093) was initially detected through infected apps on the Google Play store, and is believed to have impacted over 10,000 victims across at least 140 countries.(Citation: Trend Micro FlyTrap)

---

### [MALWARE] FakeSpy
- relevance: high (matched: fake)
- url: https://attack.mitre.org/software/S0509

- **설명**:
[FakeSpy](https://attack.mitre.org/software/S0509) is Android spyware that has been operated by the Chinese threat actor behind the Roaming Mantis campaigns.(Citation: Cybereason FakeSpy)

---

### [MALWARE] SharkBot
- relevance: medium (matched: banking, accessibility service)
- url: https://attack.mitre.org/software/S1055

- **설명**:
[SharkBot](https://attack.mitre.org/software/S1055) is a banking malware, first discovered in October 2021, that tries to initiate money transfers directly from compromised devices by abusing Accessibility Services.(Citation: nccgroup_sharkbot_0322)

---

### [MALWARE] Trojan-SMS.AndroidOS.Agent.ao
- relevance: medium (matched: sms)
- url: https://attack.mitre.org/software/S0307

- **설명**:
[Trojan-SMS.AndroidOS.Agent.ao](https://attack.mitre.org/software/S0307) is Android malware. (Citation: Kaspersky-MobileMalware)

---

### [MALWARE] Anubis
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S0422

- **설명**:
[Anubis](https://attack.mitre.org/software/S0422) is Android malware that was originally used for cyber espionage, and has been retooled as a banking trojan.(Citation: Cofense Anubis)

---

### [MALWARE] AndroRAT
- relevance: medium (matched: sms, remote access)
- url: https://attack.mitre.org/software/S0292

- **설명**:
[AndroRAT](https://attack.mitre.org/software/S0292) is an open-source remote access tool for Android devices. [AndroRAT](https://attack.mitre.org/software/S0292) is capable of collecting data, such as device location, call logs, etc., and is capable of executing actions, such as sending SMS messages and taking pictures.(Citation: Lookout-EnterpriseApps)(Citation: github_androrat)(Citation: Forcepoint BITTER Pakistan Oct 2016) It is originally available through the `The404Hacking` Github repository.(Citation: github_androrat)

---

### [MALWARE] Agent Smith
- relevance: high (matched: fraudulent)
- url: https://attack.mitre.org/software/S0440

- **설명**:
[Agent Smith](https://attack.mitre.org/software/S0440) is mobile malware that generates financial gain by replacing legitimate applications on devices with malicious versions that include fraudulent ads. As of July 2019 [Agent Smith](https://attack.mitre.org/software/S0440) had infected around 25 million devices, primarily targeting India though effects had been observed in other Asian countries as well as Saudi Arabia, the United Kingdom, and the United States.(Citation: CheckPoint Agent Smith)

---

### [MALWARE] Asacub
- relevance: medium (matched: banking, sms)
- url: https://attack.mitre.org/software/S0540

- **설명**:
[Asacub](https://attack.mitre.org/software/S0540) is a banking trojan that attempts to steal money from victims’ bank accounts. It attempts to do this by initiating a wire transfer via SMS message from compromised devices.(Citation: Securelist Asacub)

---

### [MALWARE] EventBot
- relevance: medium (matched: banking, accessibility service)
- url: https://attack.mitre.org/software/S0478

- **설명**:
[EventBot](https://attack.mitre.org/software/S0478) is an Android banking trojan and information stealer that abuses Android’s accessibility service to steal data from various applications.(Citation: Cybereason EventBot) [EventBot](https://attack.mitre.org/software/S0478) was designed to target over 200 different banking and financial applications, the majority of which are European bank and cryptocurrency exchange applications.(Citation: Cybereason EventBot)

---

### [MALWARE] GodFather
- relevance: high (matched: credential)
- url: https://attack.mitre.org/software/S1231

- **설명**:
[GodFather](https://attack.mitre.org/software/S1231) is an Android banking malware that uses virtualization to mimic legitimate applications and abuses accessibility services and other permissions to evade detection and exfiltrate sensitive data. First identified in 2020, [GodFather](https://attack.mitre.org/software/S1231) targets nearly 500 banking applications, cryptocurrency wallets, and exchanges worldwide; however, its virtualization-based attacks have primarily focused on several Turkish financial institutions. This capability enables threat actors to steal banking credentials and other sensitive account information. (Citation: ZimperiumOrtegaPratapagiri_GodFather_Jun2025)(Citation: MerkleScience_Godfather_April2023)

---

### [MALWARE] Riltok
- relevance: high (matched: phishing, credential)
- url: https://attack.mitre.org/software/S0403

- **설명**:
[Riltok](https://attack.mitre.org/software/S0403) is banking malware that uses phishing popups to collect user credentials.(Citation: Kaspersky Riltok June 2019)

---

### [MALWARE] Circles
- relevance: medium (matched: sms)
- url: https://attack.mitre.org/software/S0602

- **설명**:
[Circles](https://attack.mitre.org/software/S0602) reportedly takes advantage of Signaling System 7 (SS7) weaknesses, the protocol suite used to route phone calls, to both track the location of mobile devices and intercept voice calls and SMS messages. It can be connected to a telecommunications company’s infrastructure or purchased as a cloud service. Circles has reportedly been linked to the NSO Group.(Citation: CitizenLab Circles)

---

### [MALWARE] HummingBad
- relevance: high (matched: fraudulent)
- url: https://attack.mitre.org/software/S0322

- **설명**:
[HummingBad](https://attack.mitre.org/software/S0322) is a family of Android malware that generates fraudulent advertising revenue and has the ability to obtain root access on older, vulnerable versions of Android. (Citation: ArsTechnica-HummingBad)

---

### [MALWARE] Exobot
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S0522

- **설명**:
[Exobot](https://attack.mitre.org/software/S0522) is Android banking malware, primarily targeting financial institutions in Germany, Austria, and France.(Citation: Threat Fabric Exobot)

---

### [MALWARE] FjordPhantom
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S1208

- **설명**:
[FjordPhantom](https://attack.mitre.org/software/S1208) is a malicious Android application first discovered in September 2024 with targets in Southeast Asia, specifically Indonesia, Thailand, and Vietnam. [FjordPhantom](https://attack.mitre.org/software/S1208) was distributed through email and messaging applications. Once installed, the application launches a virtualization solution to steal important information, such as bank accounts, and to manipulate the user interface. The malicious activity from the virtualization solution runs alongside legitimate banking applications.(Citation: Promon FjordPhantom Oct2024)

---

### [MALWARE] Android/Chuli.A
- relevance: high (matched: phishing, spearphishing)
- url: https://attack.mitre.org/software/S0304

- **설명**:
[Android/Chuli.A](https://attack.mitre.org/software/S0304) is Android malware that was delivered to activist groups via a spearphishing email with an attachment. (Citation: Kaspersky-WUC)

---

### [MALWARE] Charger
- relevance: medium (matched: sms)
- url: https://attack.mitre.org/software/S0323

- **설명**:
[Charger](https://attack.mitre.org/software/S0323) is Android malware that steals steals contacts and SMS messages from the user's device. It can also lock the device and demand ransom payment if it receives admin permissions. (Citation: CheckPoint-Charger)

---

### [MALWARE] Drinik
- relevance: medium (matched: banking, sms)
- url: https://attack.mitre.org/software/S1054

- **설명**:
[Drinik](https://attack.mitre.org/software/S1054) is an evolving Android banking trojan that was observed targeting customers of around 27 banks in India in August 2021. Initially seen as an SMS stealer in 2016, [Drinik](https://attack.mitre.org/software/S1054) resurfaced as a banking trojan with more advanced capabilities included in subsequent versions between September 2021 and August 2022.(Citation: cyble_drinik_1022)

---

### [MALWARE] Trojan-SMS.AndroidOS.OpFake.a
- relevance: high (matched: fake)
- url: https://attack.mitre.org/software/S0308

- **설명**:
[Trojan-SMS.AndroidOS.OpFake.a](https://attack.mitre.org/software/S0308) is Android malware. (Citation: Kaspersky-MobileMalware)

---

### [MALWARE] SilkBean
- relevance: medium (matched: remote access)
- url: https://attack.mitre.org/software/S0549

- **설명**:
[SilkBean](https://attack.mitre.org/software/S0549) is a piece of Android surveillanceware containing comprehensive remote access tool (RAT) functionality that has been used in targeting of the Uyghur ethnic group.(Citation: Lookout Uyghur Campaign)

---

### [MALWARE] TERRACOTTA
- relevance: high (matched: fraudulent)
- url: https://attack.mitre.org/software/S0545

- **설명**:
[TERRACOTTA](https://attack.mitre.org/software/S0545) is an ad fraud botnet that has been capable of generating over 2 billion fraudulent requests per week.(Citation: WhiteOps TERRACOTTA)

---

### [MALWARE] Escobar
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S1092

- **설명**:
[Escobar](https://attack.mitre.org/software/S1092) is an Android banking trojan, first detected in March 2021, believed to be a new variant of AbereBot.(Citation: Bleeipng Computer Escobar)

---

### [MALWARE] Crocodilus
- relevance: medium (matched: banking)
- url: https://attack.mitre.org/software/S9004

- **설명**:
[Crocodilus](https://attack.mitre.org/software/S9004) is an Android banking Trojan that was discovered in March 2025. [Crocodilus](https://attack.mitre.org/software/S9004) targeted users worldwide, including Turkey, Poland, Argentina, Brazil, Spain, the United States, Indonesia and India. [Crocodilus](https://attack.mitre.org/software/S9004) has been customized based on the target location. For example, [Crocodilus](https://attack.mitre.org/software/S9004) mimicked major Turkish and Spanish banks for users in Turkey and Spain, while users in Poland saw Facebook advertisements that promoted [Crocodilus](https://attack.mitre.org/software/S9004) to claim bonus points.(Citation: ThreatFabric_Crocodilus_March2025)(Citation: ThreatFabric_Crocodilus_June2025)

---

### [MALWARE] Android/SpyAgent
- relevance: high (matched: phishing, fake)
- url: https://attack.mitre.org/software/S1214

- **설명**:
[Android/SpyAgent](https://attack.mitre.org/software/S1214) is a variant of spyware in the MoqHao phishing campaign primarily targeting Korean and Japanese users.(Citation: McAfee MoqHao 2019) Fake security applications were used to target Japanese users, while fake police applications were used to target Korean users. Both fake applications have common C2 commands and share the same crash report key on a cloud service.(Citation: McAfee MoqHao 2019)

---

### [MALWARE] FluBot
- relevance: high (matched: phishing)
- url: https://attack.mitre.org/software/S1067

- **설명**:
[FluBot](https://attack.mitre.org/software/S1067) is a multi-purpose mobile banking malware that was first observed in Spain in late 2020. It primarily spread through European countries using a variety of SMS phishing messages in multiple languages.(Citation: proofpoint_flubot_0421)(Citation: bitdefender_flubot_0524) An international law enforcement operation of 11 countries eventually disrupted the spread of [FluBot](https://attack.mitre.org/software/S1067).(Citation: Europol FluBot Jun2022)

---

### [MALWARE] TianySpy
- relevance: high (matched: phishing, credential)
- url: https://attack.mitre.org/software/S1056

- **설명**:
[TianySpy](https://attack.mitre.org/software/S1056) is a mobile malware primarily spread by SMS phishing between September 30 and October 12, 2021. [TianySpy](https://attack.mitre.org/software/S1056) is believed to have targeted credentials associated with membership websites of major Japanese telecommunication services.(Citation: trendmicro_tianyspy_0122)

---

### [MALWARE] Gustuff
- relevance: high (matched: credential)
- url: https://attack.mitre.org/software/S0406

- **설명**:
[Gustuff](https://attack.mitre.org/software/S0406) is mobile malware designed to steal users' banking and virtual currency credentials.(Citation: Talos Gustuff Apr 2019)

---

### [ATTACK-PATTERN] Adversary-in-the-Middle
- relevance: high (matched: spoof, malicious app, malicious application)
- url: https://attack.mitre.org/techniques/T1565/002

- **설명**:
Adversaries may attempt to position themselves between two or more networked devices to support follow-on behaviors such as [Transmitted Data Manipulation](https://attack.mitre.org/techniques/T1565/002) or [Endpoint Denial of Service](https://attack.mitre.org/techniques/T1642).

[Adversary-in-the-Middle](https://attack.mitre.org/techniques/T1638) can be achieved through several mechanisms. For example, a malicious application may register itself as a VPN client, effectively redirecting device traffic to adversary-owned resources. Registering as a VPN client requires user consent on both Android and iOS; additionally, a special entitlement granted by Apple is needed for iOS devices. Alternatively, a malicious application with escalation privileges may utilize those privileges to gain access to network traffic.

 Specific to Android devices, adversary-in-the-disk is a type of AiTM attack where adversaries monitor and manipulate data that is exchanged between applications and external storage.(Citation: mitd_kaspersky)(Citation: mitd_checkpoint)(Citation: mitd_checkpoint_research) To accomplish this, a malicious application firsts requests for access to multimedia files on the device (`READ_EXTERNAL STORAGE` and `WRITE_EXTERNAL_STORAGE`), then the application reads data on the device and/or writes malware to the device. Though the request for access is common, when used maliciously, adversaries may access files and other sensitive data due to abusing the permission. Multiple applications were shown to be vulnerable against this attack; however, scrutiny of permissions and input validations may mitigate this attack.

Outside of a mobile device, adversaries may be able to capture traffic by employing a rogue base station or Wi-Fi access point. These devices will allow adversaries to capture network traffic after it has left the device, while it is flowing to its destination. On a local network, enterprise techniques could be used, such as [ARP Cache Poisoning](https://attack.mitre.org/techniques/T1557/002) or [DHCP Spoofing](https://attack.mitre.org/techniques/T1557/003).

If applications properly encrypt their network traffic, sensitive data may not be accessible to adversaries, depending on the point of capture. For example, properly implementing Apple’s Application Transport Security (ATS) and Android’s Network Security Configuration (NSC) may prevent sensitive data leaks.(Citation: NSC_Android)

---

### [ATTACK-PATTERN] Abuse Elevation Control Mechanism
- relevance: medium (matched: sms)

- **설명**:
Adversaries may circumvent mechanisms designed to control elevated privileges to gain higher-level permissions. Most modern systems contain native elevation control mechanisms that are intended to limit privileges that a user can gain on a machine. Authorization has to be granted to specific users in order to perform tasks that are designated as higher risk. An adversary can use several methods to take advantage of built-in control mechanisms in order to escalate privileges on a system.

---

### [ATTACK-PATTERN] Remote Access Software
- relevance: medium (matched: remote access)

- **설명**:
Adversaries may use legitimate remote access software, such as `VNC`, `TeamViewer`, `AirDroid`, `AirMirror`, etc., to establish an interactive command and control channel to target mobile devices.

Remote access applications may be installed and used post-compromise as an alternate communication channel for redundant access or as a way to establish an interactive remote session with the target device. They may also be used as a component of malware to establish a reverse connection to an adversary-controlled system or service. Installation of remote access tools may also include persistence.

---

### [ATTACK-PATTERN] Uninstall Malicious Application
- relevance: high (matched: malicious app, malicious application)

- **설명**:
Adversaries may include functionality in malware that uninstalls the malicious application from the device. This can be achieved by:

* Abusing device owner permissions to perform silent uninstallation using device owner API calls.
* Abusing root permissions to delete files from the filesystem.
* Abusing the accessibility service. This requires sending an intent to the system to request uninstallation, and then abusing the accessibility service to click the proper places on the screen to confirm uninstallation.

---

### [ATTACK-PATTERN] Indicator Removal on Host
- relevance: high (matched: malicious app, malicious application)

- **설명**:
Adversaries may delete, alter, or hide generated artifacts on a device, including files, jailbreak status, or the malicious application itself. These actions may interfere with event collection, reporting, or other notifications used to detect intrusion activity. This may compromise the integrity of mobile security solutions by causing notable events or information to go unreported.

---

### [ATTACK-PATTERN] Supply Chain Compromise
- relevance: medium (matched: sms)

- **설명**:
Adversaries may manipulate products or product delivery mechanisms prior to receipt by a final consumer for the purpose of data or system compromise.

Supply chain compromise can take place at any stage of the supply chain including:

* Manipulation of development tools
* Manipulation of a development environment
* Manipulation of source code repositories (public or private)
* Manipulation of source code in open-source dependencies
* Manipulation of software update/distribution mechanisms
* Compromised/infected system images
* Replacement of legitimate software with modified versions
* Sales of modified/counterfeit products to legitimate distributors
* Shipment interdiction

While supply chain compromise can impact any component of hardware or software, attackers looking to gain execution have often focused on malicious additions to legitimate software in software distribution or update channels. Targeting may be specific to a desired victim set or malicious software may be distributed to a broad set of consumers but only move on to additional tactics on specific victims.  Popular open source projects that are used as dependencies in many applications may also be targeted as a means to add malicious code to users of the dependency, specifically with the widespread usage of third-party advertising libraries.(Citation: Grace-Advertisement)(Citation: NowSecure-RemoteCode)

---

### [ATTACK-PATTERN] Impersonate SS7 Nodes
- relevance: high (matched: impersonat)

- **설명**:
Adversaries may exploit the lack of authentication in signaling system network nodes to track the location of mobile devices by impersonating a node.(Citation: Engel-SS7)(Citation: Engel-SS7-2008)(Citation: 3GPP-Security)(Citation: Positive-SS7)(Citation: CSRIC5-WG10-FinalReport)

By providing the victim’s MSISDN (phone number) and impersonating network internal nodes to query subscriber information from other nodes, adversaries may use data collected from each hop to eventually determine the device’s geographical cell area or nearest cell tower.(Citation: Engel-SS7)

---

### [ATTACK-PATTERN] Impair Defenses
- relevance: medium (matched: sms)

- **설명**:
Adversaries may maliciously modify components of a victim environment in order to hinder or disable defensive mechanisms. This not only involves impairing preventative defenses, such as anti-virus, but also detection capabilities that defenders can use to audit activity and identify malicious behavior. This may span both native defenses as well as supplemental capabilities installed by users or mobile endpoint administrators.

---

### [ATTACK-PATTERN] Abuse Accessibility Features
- relevance: high (matched: credential)
- url: https://attack.mitre.org/techniques/T1417/001

- **설명**:
Adversaries may abuse accessibility features in Android devices to steal sensitive data and to spread malware to other devices. Accessibility features in Android are designed to assist users with disabilities, performing a variety of tasks, such as using Action Blocks to control lightbulbs, and changing the device’s user interface, such as changing the font size and adjusting contract or colors.(Citation: Google_AndroidAcsOverview)

One example of how adversaries abuse accessibility features is overlaying an HTML object mimicking a legitimate login screen. The user types their credentials in the overlay HTML object, which is then sent to the adversaries.(Citation: SahinSRLabs_FluBot_Dec2021)

Another example is a malicious accessibility feature acting as a keylogger. The keylogger monitors changes on the EditText fields and sends it to the adversaries.(Citation: SahinSRLabs_FluBot_Dec2021) This method of attack is also described in [Keylogging](https://attack.mitre.org/techniques/T1417/001); whereas [Abuse Accessibility Features](https://attack.mitre.org/techniques/T1453) captures the overall abuse of accessibility features.

---

### [ATTACK-PATTERN] Steal Application Access Token
- relevance: high (matched: credential, social engineering)

- **설명**:
Adversaries can steal user application access tokens as a means of acquiring credentials to access remote systems and resources. This can occur through social engineering or URI hijacking and typically requires user action to grant access, such as through a system “Open With” dialogue.

Application access tokens are used to make authorized API requests on behalf of a user and are commonly used as a way to access resources in cloud-based applications and software-as-a-service (SaaS).(Citation: Auth0 - Why You Should Always Use Access Tokens to Secure APIs Sept 2019) OAuth is one commonly implemented framework used to issue tokens to users for access to systems. An application desiring access to cloud-based services or protected APIs can gain entry through OAuth 2.0 using a variety of authorization protocols. An example of a commonly-used sequence is Microsoft's Authorization Code Grant flow.(Citation: Microsoft Identity Platform Protocols May 2019)(Citation: Microsoft - OAuth Code Authorization flow - June 2019) An OAuth access token enables a third-party application to interact with resources containing user data in the ways requested without requiring user credentials.

---

### [ATTACK-PATTERN] Disable or Modify Tools
- relevance: medium (matched: device administrator)

- **설명**:
Adversaries may disable security tools to avoid potential detection of their tools and activities. This can take the form of disabling security software, modifying SELinux configuration, or other methods to interfere with security tools scanning or reporting information. This is typically done by abusing device administrator permissions or using system exploits to gain root access to the device to modify protected system files.

---

### [ATTACK-PATTERN] Broadcast Receivers
- relevance: high (matched: malicious app, malicious application)

- **설명**:
Adversaries may establish persistence using system mechanisms that trigger execution based on specific events. Mobile operating systems have means to subscribe to events such as receiving an SMS message, device boot completion, or other device activities.

An intent is a message passed between Android applications or system components. Applications can register to receive broadcast intents at runtime, which are system-wide intents delivered to each app when certain events happen on the device, such as network changes or the user unlocking the screen. Malicious applications can then trigger certain actions within the app based on which broadcast intent was received.

In addition to Android system intents, malicious applications can register for intents broadcasted by other applications. This allows the malware to respond based on actions in other applications. This behavior typically indicates a more intimate knowledge, or potentially the targeting of specific devices, users, or applications.

In Android 8 (API level 26), broadcast intent behavior was changed, limiting the implicit intents that applications can register for in the manifest. In most cases, applications that register through the manifest will no longer receive the broadcasts. Now, applications must register context-specific broadcast receivers while the user is actively using the app.(Citation: Android Changes to System Broadcasts)

---

### [ATTACK-PATTERN] Access Notifications
- relevance: high (matched: credential)

- **설명**:
Adversaries may collect data within notifications sent by the operating system or other applications. Notifications may contain sensitive data such as one-time authentication codes sent over SMS, email, or other mediums. In the case of Credential Access, adversaries may attempt to intercept one-time code sent to the device. Adversaries can also dismiss notifications to prevent the user from noticing that the notification has arrived and can trigger action buttons contained within notifications.(Citation: ESET 2FA Bypass)

---

### [ATTACK-PATTERN] GUI Input Capture
- relevance: high (matched: phishing, credential, fake, malicious app, malicious application, impersonat)

- **설명**:
Adversaries may mimic common operating system GUI components to prompt users for sensitive information with a seemingly legitimate prompt. The operating system and installed applications often have legitimate needs to prompt the user for sensitive information such as account credentials, bank account information, or Personally Identifiable Information (PII). Compared to traditional PCs, the constrained display size of mobile devices may impair the ability to provide users with contextual information, making users more susceptible to this technique’s use.(Citation: Felt-PhishingOnMobileDevices)

There are several approaches adversaries may use to mimic this functionality. Adversaries may impersonate the identity of a legitimate application (e.g. use the same application name and/or icon) and, when installed on the device, may prompt the user for sensitive information.(Citation: eset-finance) Adversaries may also send fake device notifications to the user that may trigger the display of an input prompt when clicked.(Citation: Group IB Gustuff Mar 2019)

Additionally, adversaries may display a prompt on top of a running, legitimate application to trick users into entering sensitive information into a malicious application rather than the legitimate application. Typically, adversaries need to know when the targeted application and the individual activity within the targeted application is running in the foreground to display the prompt at the proper time. Adversaries can abuse Android’s accessibility features to determine which application is currently in the foreground.(Citation: ThreatFabric Cerberus) Two known approaches to displaying a prompt include:

* Adversaries start a new activity on top of a running legitimate application.(Citation: Felt-PhishingOnMobileDevices)(Citation: Hassell-ExploitingAndroid) Android 10 places new restrictions on the ability for an application to start a new activity on top of another application, which may make it more difficult for adversaries to utilize this technique.(Citation: Android Background)
* Adversaries create an application overlay window on top of a running legitimate application. Applications must hold the `SYSTEM_ALERT_WINDOW` permission to create overlay windows. This permission is handled differently than typical Android permissions and, at least under certain conditions, is automatically granted to applications installed from the Google Play Store.(Citation: Cloak and Dagger)(Citation: NowSecure Android Overlay)(Citation: Skycure-Accessibility) The `SYSTEM_ALERT_WINDOW` permission and its associated ability to create application overlay windows are expected to be deprecated in a future release of Android in favor of a new API.(Citation: XDA Bubbles)

---

### [ATTACK-PATTERN] Exploitation for Client Execution
- relevance: high (matched: phishing, drive-by)
- url: https://attack.mitre.org/techniques/T1456

- **설명**:
Adversaries may exploit software vulnerabilities in client applications to execute code. Vulnerabilities can exist in software due to insecure coding practices that can lead to unanticipated behavior. Adversaries may take advantage of certain vulnerabilities through targeted exploitation for the purpose of arbitrary code execution. Oftentimes the most valuable exploits to an offensive toolkit are those that can be used to obtain code execution on a remote system because they can be used to gain access to that system. Users will expect to see files related to the applications they commonly used to do work, so they are a useful target for exploit research and development because of their high utility.

Adversaries may use device-based zero-click exploits for code execution. These exploits are powerful because there is no user interaction required for code execution.

### SMS/iMessage Delivery

SMS and iMessage in iOS are common targets through [Drive-By Compromise](https://attack.mitre.org/techniques/T1456), [Phishing](https://attack.mitre.org/techniques/T1660), etc. Adversaries may use embed malicious links, files, etc. in SMS messages or iMessages. Mobile devices may be compromised through one-click exploits, where the victim must interact with a text message, or zero-click exploits, where no user interaction is required.

### AirDrop

Unique to iOS, AirDrop is a network protocol that allows iOS users to transfer files between iOS devices. Before patches from Apple were released, on iOS 13.4 and earlier, adversaries may force the Apple Wireless Direct Link (AWDL) interface to activate, then exploit a buffer overflow to gain access to the device and run as root without interaction from the user.

---

### [ATTACK-PATTERN] Foreground Persistence
- relevance: high (matched: malicious app, malicious application)

- **설명**:
Adversaries may abuse Android's `startForeground()` API method to maintain continuous sensor access. Beginning in Android 9, idle applications running in the background no longer have access to device sensors, such as the camera, microphone, and gyroscope.(Citation: Android-SensorsOverview) Applications can retain sensor access by running in the foreground, using Android’s `startForeground()` API method. This informs the system that the user is actively interacting with the application, and it should not be killed. The only requirement to start a foreground service is showing a persistent notification to the user.(Citation: Android-ForegroundServices)

Malicious applications may abuse the `startForeground()` API method to continue running in the foreground, while presenting a notification to the user pretending to be a genuine application. This would allow unhindered access to the device’s sensors, assuming permission has been previously granted.(Citation: BlackHat Sutter Android Foreground 2019)

Malicious applications may also abuse the `startForeground()` API to inform the Android system that the user is actively interacting with the application, thus preventing it from being killed by the low memory killer.(Citation: TrendMicro-Yellow Camera)

---

### [ATTACK-PATTERN] Replication Through Removable Media
- relevance: high (matched: malicious app, malicious application)

- **설명**:
Adversaries may move onto devices by exploiting or copying malware to devices connected via USB. In the case of Lateral Movement, adversaries may utilize the physical connection of a device to a compromised or malicious charging station or PC to bypass application store requirements and install malicious applications directly.(Citation: Lau-Mactans) In the case of Initial Access, adversaries may attempt to exploit the device via the connection to gain access to data stored on the device.(Citation: Krebs-JuiceJacking) Examples of this include:

* Exploiting insecure bootloaders in a Nexus 6 or 6P device over USB and gaining the ability to perform actions including intercepting phone calls, intercepting network traffic, and obtaining the device physical location.(Citation: IBM-NexusUSB)
* Exploiting weakly-enforced security boundaries in Android devices such as the Google Pixel 2 over USB.(Citation: GoogleProjectZero-OATmeal)
* Products from Cellebrite and Grayshift purportedly that can exploit some iOS devices using physical access to the data port to unlock the passcode.(Citation: Computerworld-iPhoneCracking)

---

### [ATTACK-PATTERN] Screen Capture
- relevance: high (matched: credential)

- **설명**:
Adversaries may use screen capture to collect additional information about a target device, such as applications running in the foreground, user data, credentials, or other sensitive information. Applications running in the background can capture screenshots or videos of another application running in the foreground by using the Android `MediaProjectionManager` (generally requires the device user to grant consent).(Citation: Fortinet screencap July 2019)(Citation: Android ScreenCap1 2019) Background applications can also use Android accessibility services to capture screen contents being displayed by a foreground application.(Citation: Lookout-Monokle) An adversary with root access or Android Debug Bridge (adb) access could call the Android `screencap` or `screenrecord` commands.(Citation: Android ScreenCap2 2019)(Citation: Trend Micro ScreenCap July 2015)

---

### [ATTACK-PATTERN] Transmitted Data Manipulation
- relevance: high (matched: malicious app, malicious application)
- url: https://attack.mitre.org/techniques/T1641/001

- **설명**:
Adversaries may alter data en route to storage or other systems in order to manipulate external outcomes or hide activity. By manipulating transmitted data, adversaries may attempt to affect a business process, organizational understanding, or decision making.

Manipulation may be possible over a network connection or between system processes where there is an opportunity to deploy a tool that will intercept and change information. The type of modification and the impact it will have depends on the target transmission mechanism as well as the goals and objectives of the adversary. For complex systems, an adversary would likely need special expertise and possibly access to specialized software related to the system, typically gained through a prolonged information gathering campaign, in order to have the desired impact.

One method to achieve [Transmitted Data Manipulation](https://attack.mitre.org/techniques/T1641/001) is by modifying the contents of the device clipboard. Malicious applications may monitor clipboard activity through the `ClipboardManager.OnPrimaryClipChangedListener` interface on Android to determine when clipboard contents have changed. Listening to clipboard activity, reading clipboard contents, and modifying clipboard contents requires no explicit application permissions and can be performed by applications running in the background. However, this behavior has changed with the release of Android 10.

Adversaries may use [Transmitted Data Manipulation](https://attack.mitre.org/techniques/T1641/001) to replace text prior to being pasted. For example, replacing a copied Bitcoin wallet address with a wallet address that is under adversarial control.

[Transmitted Data Manipulation](https://attack.mitre.org/techniques/T1641/001) was seen within the Android/Clipper.C trojan. This sample was detected by ESET in an application distributed through the Google Play Store targeting cryptocurrency wallet numbers.(Citation: ESET Clipboard Modification February 2019)

---

### [ATTACK-PATTERN] Compromise Software Dependencies and Development Tools
- relevance: medium (matched: sms)

- **설명**:
Adversaries may manipulate products or product delivery mechanisms prior to receipt by a final consumer for the purpose of data or system compromise. Applications often depend on external software to function properly. Popular open source projects that are used as dependencies in many applications may be targeted as a means to add malicious code to users of the dependency.(Citation: Grace-Advertisement)

---

### [ATTACK-PATTERN] URI Hijacking
- relevance: high (matched: phishing)

- **설명**:
Adversaries may register Uniform Resource Identifiers (URIs) to intercept sensitive data.

Applications regularly register URIs with the operating system to act as a response handler for various actions, such as logging into an app using an external account via single sign-on. This allows redirections to that specific URI to be intercepted by the application. If an adversary were to register for a URI that was already in use by a genuine application, the adversary may be able to intercept data intended for the genuine application or perform a phishing attack against the genuine application. Intercepted data may include OAuth authorization codes or tokens that could be used by the adversary to gain access to protected resources.(Citation: Trend Micro iOS URL Hijacking)(Citation: IETF-PKCE)

---

### [ATTACK-PATTERN] Subvert Trust Controls
- relevance: medium (matched: sms)

- **설명**:
Adversaries may undermine security controls that will either warn users of untrusted activity or prevent execution of untrusted applications. Operating systems and security products may contain mechanisms to identify programs or websites as possessing some level of trust. Examples of such features include: an app being allowed to run because it is signed by a valid code signing certificate; an OS prompt alerting the user that an app came from an untrusted source; or getting an indication that you are about to connect to an untrusted site. The method adversaries use will depend on the specific mechanism they seek to subvert.

---

### [ATTACK-PATTERN] Keychain
- relevance: high (matched: credential)

- **설명**:
Adversaries may collect keychain data from an iOS device to acquire credentials. Keychains are the built-in way for iOS to keep track of users' passwords and credentials for many services and features such as Wi-Fi passwords, websites, secure notes, certificates, private keys, and VPN credentials.

On the device, the keychain database is stored outside of application sandboxes to prevent unauthorized access to the raw data. Standard iOS APIs allow applications access to their own keychain contained within the database. By utilizing a privilege escalation exploit or existing root access, adversaries can access the entire encrypted database.(Citation: Apple Keychain Services)(Citation: Elcomsoft Decrypt Keychain)

---

### [ATTACK-PATTERN] Virtualization Solution
- relevance: high (matched: credential)

- **설명**:
Adversaries may carry out malicious operations using virtualization solutions to escape from Android sandboxes and to avoid detection. Android uses sandboxes to separate resources and code execution between applications and the operating system.(Citation: Android Application Sandbox) There are a few virtualization solutions available on Android, such as the Android Virtualization Framework (AVF).(Citation: Android AVF Overview)

Through virtualization solutions, adversaries may execute malicious operations without user knowledge. For example, adversaries may mimic a legitimate banking application’s functionalities in a virtual environment, thanks to the virtualization solution, while malicious code captures credentials.

---

### [ATTACK-PATTERN] Device Administrator Permissions
- relevance: medium (matched: device administrator)
- url: https://attack.mitre.org/techniques/T1642

- **설명**:
Adversaries may abuse Android’s device administration API to obtain a higher degree of control over the device. By abusing the API, adversaries can perform several nefarious actions, such as resetting the device’s password for [Endpoint Denial of Service](https://attack.mitre.org/techniques/T1642), factory resetting the device for [File Deletion](https://attack.mitre.org/techniques/T1630/002) and to delete any traces of the malware, disabling all the device’s cameras, or to make it more difficult to uninstall the app.

Device administrators must be approved by the user at runtime, with a system popup showing which actions have been requested by the app. In conjunction with other techniques, such as [Input Injection](https://attack.mitre.org/techniques/T1516), an app can programmatically grant itself administrator permissions without any user input.

---

### [ATTACK-PATTERN] Linked Devices
- relevance: high (matched: qr code, phishing)
- url: https://attack.mitre.org/techniques/T1660

- **설명**:
Adversaries may abuse the “linked devices” feature on messaging applications, such as Signal and WhatsApp, to register the user’s account to an adversary-controlled device. By abusing the “linked devices” feature, adversaries may achieve and maintain persistence through the user’s account, may collect information, such as the user’s messages and contacts list, and may send future messages from the linked device.

Signal is a messaging application that uses the open-source Signal Protocol to encrypt messages and calls; similarly, WhatsApp is a messaging application that has end-to-end encryption and other security measures to protect messages and calls. Both applications have a “linked devices” feature that allows users to access their Signal and/or WhatsApp accounts from different devices, such as a Windows or Mac desktop, an iPad or an Android tablet.(Citation: WhatsApp_LinkDevice_NoDate)(Citation: Signal_LinkedDevices_NoDate)

Adversaries may use [Phishing](https://attack.mitre.org/techniques/T1660) techniques to trick the user into scanning a quick-response (QR) code, which is used to link the user’s Signal and/or WhatsApp account to an adversary-controlled device. For example, adversaries may masquerade QR codes as group invites, security alerts or as legitimate instructions for pairing linked devices.
Upon scanning the QR code in Signal, users may click on the “Transfer Message History” option to sync the linked devices, which may allow adversaries to collect more information about the user. Upon scanning the QR code in WhatsApp, the user’s device will automatically send an end-to-end encrypted copy of recent message history to the adversary-controlled device.

---

### [ATTACK-PATTERN] SIM Card Swap
- relevance: high (matched: phishing, social engineering, impersonat)
- url: https://attack.mitre.org/techniques/T1660

- **설명**:
Adversaries may gain access to mobile devices through transfers or swaps from victims’ phone numbers to adversary-controlled SIM cards and mobile devices.(Citation: ATT SIM Swap Scams)(Citation: Verizon SIM Swapping)

The typical process is as follows:

1. Adversaries will first gather information about victims through [Phishing](https://attack.mitre.org/techniques/T1660), social engineering, data breaches, or other avenues.
2. Adversaries will then impersonate victims as they contact mobile carriers to request for the SIM swaps. For example, adversaries would provide victims’ name and address to mobile carriers; once authenticated, adversaries would request for victims’ phone numbers to be transferred to adversary-controlled SIM cards.
3. Once completed, victims will lose mobile data, such as text messages and phone calls, on their mobile devices. In turn, adversaries will receive mobile data that was intended for the victims.

Adversaries may use the intercepted SMS messages to log into online accounts that use SMS-based authentication. Specifically, adversaries may use SMS-based authentication to log into banking and/or cryptocurrency accounts, then transfer funds to adversary-controlled wallets.

---

### [ATTACK-PATTERN] Input Capture
- relevance: high (matched: credential)
- url: https://attack.mitre.org/techniques/T1417/001

- **설명**:
Adversaries may use methods of capturing user input to obtain credentials or collect information. During normal device usage, users often provide credentials to various locations, such as login pages/portals or system dialog boxes. Input capture mechanisms may be transparent to the user (e.g. [Keylogging](https://attack.mitre.org/techniques/T1417/001)) or rely on deceiving the user into providing input into what they believe to be a genuine application prompt (e.g. [GUI Input Capture](https://attack.mitre.org/techniques/T1417/002)).

---

### [ATTACK-PATTERN] Generate Traffic from Victim
- relevance: medium (matched: sms)

- **설명**:
Adversaries may generate outbound traffic from devices. This is typically performed to manipulate external outcomes, such as to achieve carrier billing fraud or to manipulate app store rankings or ratings. Outbound traffic is typically generated as SMS messages or general web traffic, but may take other forms as well.

If done via SMS messages, Android apps must hold the `SEND_SMS` permission. Additionally, sending an SMS message requires user consent if the recipient is a premium number. Applications cannot send SMS messages on iOS

---

### [ATTACK-PATTERN] Device Lockout
- relevance: medium (matched: overlay, device administrator)

- **설명**:
An adversary may seek to inhibit user interaction by locking the legitimate user out of the device. This is typically accomplished by requesting device administrator permissions and then locking the screen using `DevicePolicyManager.lockNow()`. Other novel techniques for locking the user out of the device have been observed, such as showing a persistent overlay, using carefully crafted “call” notification screens, and locking HTML pages in the foreground. These techniques can be very difficult to get around, and typically require booting the device into safe mode to uninstall the malware.(Citation: Microsoft MalLockerB)(Citation: Talos GPlayed)(Citation: securelist rotexy 2018)

Prior to Android 7, device administrators were able to reset the device lock passcode to prevent the user from unlocking the device. The release of Android 7 introduced updates that only allow device or profile owners (e.g. MDMs) to reset the device’s passcode.(Citation: Android resetPassword)

---

### [ATTACK-PATTERN] Keylogging
- relevance: high (matched: credential)

- **설명**:
Adversaries may log user keystrokes to intercept credentials or other information from the user as the user types them.

Some methods of keylogging include:

* Masquerading as a legitimate third-party keyboard to record user keystrokes.(Citation: Zeltser-Keyboard) On both Android and iOS, users must explicitly authorize the use of third-party keyboard apps. Users should be advised to use extreme caution before granting this authorization when it is requested.
* Abusing accessibility features. On Android, adversaries may abuse accessibility features to record keystrokes by registering an `AccessibilityService` class, overriding the `onAccessibilityEvent` method, and listening for the `AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED` event type. The event object passed into the function will contain the data that the user typed.
*Additional methods of keylogging may be possible if root access is available.

---

### [ATTACK-PATTERN] SMS Control
- relevance: high (matched: malicious app, malicious application)

- **설명**:
Adversaries may delete, alter, or send SMS messages without user authorization. This could be used to hide C2 SMS messages, spread malware, or various external effects.

This can be accomplished by requesting the `RECEIVE_SMS` or `SEND_SMS` permissions depending on what the malware is attempting to do. If the app is set as the default SMS handler on the device, the `SMS_DELIVER` broadcast intent can be registered, which allows the app to write to the SMS content provider. The content provider directly modifies the messaging database on the device, which could allow malicious applications with this ability to insert, modify, or delete arbitrary messages on the device.(Citation: SMS KitKat)(Citation: Android SmsProvider)

---

### [ATTACK-PATTERN] Wi-Fi Discovery
- relevance: high (matched: credential)
- url: https://attack.mitre.org/tactics/TA0032

- **설명**:
Adversaries may search for information about Wi-Fi networks, such as network names and passwords, on compromised systems. Adversaries may use Wi-Fi information as part of [Discovery](https://attack.mitre.org/tactics/TA0032) or [Credential Access](https://attack.mitre.org/tactics/TA0031) activity to support both ongoing and future campaigns.

---

### [ATTACK-PATTERN] Clipboard Data
- relevance: high (matched: malicious app, malicious application)

- **설명**:
Adversaries may abuse clipboard manager APIs to obtain sensitive information copied to the device clipboard. For example, passwords being copied and pasted from a password manager application could be captured by a malicious application installed on the device.(Citation: Fahl-Clipboard)

On Android, applications can use the `ClipboardManager.OnPrimaryClipChangedListener()` API to register as a listener and monitor the clipboard for changes. However, starting in Android 10, this can only be used if the application is in the foreground, or is set as the device’s default input method editor (IME).(Citation: Github Capture Clipboard 2019)(Citation: Android 10 Privacy Changes)

On iOS, this can be accomplished by accessing the `UIPasteboard.general.string` field. However, starting in iOS 14, upon accessing the clipboard, the user will be shown a system notification if the accessed text originated in a different application. For example, if the user copies the text of an iMessage from the Messages application, the notification will read “application_name has pasted from Messages” when the text was pasted in a different application.(Citation: UIPPasteboard)

---

### [ATTACK-PATTERN] SMS Messages
- relevance: medium (matched: sms)
- url: https://attack.mitre.org/techniques/T1636/004

- **설명**:
Adversaries may utilize standard operating system APIs to gather SMS messages. On Android, this can be accomplished using the SMS Content Provider. iOS provides no standard API to access SMS messages.

If the device has been jailbroken or rooted, an adversary may be able to access [SMS Messages](https://attack.mitre.org/techniques/T1636/004) without the user’s knowledge or approval.

---

### [ATTACK-PATTERN] Credentials from Password Store
- relevance: high (matched: credential)

- **설명**:
Adversaries may search common password storage locations to obtain user credentials. Passwords can be stored in several places on a device, depending on the operating system or application holding the credentials. There are also specific applications that store passwords to make it easier for users to manage and maintain. Once credentials are obtained, they can be used to perform lateral movement and access restricted information.

---

### [ATTACK-PATTERN] Input Injection
- relevance: high (matched: malicious app, malicious application)
- url: https://attack.mitre.org/techniques/T1516

- **설명**:
A malicious application can inject input to the user interface to mimic user interaction through the abuse of Android's accessibility APIs.

[Input Injection](https://attack.mitre.org/techniques/T1516) can be achieved using any of the following methods:

* Mimicking user clicks on the screen, for example to steal money from a user's PayPal account.(Citation: android-trojan-steals-paypal-2fa)
* Injecting global actions, such as `GLOBAL_ACTION_BACK` (programatically mimicking a physical back button press), to trigger actions on behalf of the user.(Citation: Talos Gustuff Apr 2019)
* Inserting input into text fields on behalf of the user. This method is used legitimately to auto-fill text fields by applications such as password managers.(Citation: bitwarden autofill logins)

---

### [ATTACK-PATTERN] Compromise Application Executable
- relevance: high (matched: malicious app, malicious application)

- **설명**:
Adversaries may modify applications installed on a device to establish persistent access to a victim. These malicious modifications can be used to make legitimate applications carry out adversary tasks when these applications are in use.

There are multiple ways an adversary can inject malicious code into applications. One method is by taking advantages of device vulnerabilities, the most well-known being Janus, an Android vulnerability that allows adversaries to add extra bytes to APK (application) and DEX (executable) files without affecting the file's signature. By being able to add arbitrary bytes to valid applications, attackers can seamlessly inject code into genuine executables without the user's knowledge.(Citation: Guardsquare Janus)

Adversaries may also rebuild applications to include malicious modifications. This can be achieved by decompiling the genuine application, merging it with the malicious code, and recompiling it.(Citation: CheckPoint Agent Smith)

Adversaries may also take action to conceal modifications to application executables and bypass user consent. These actions include altering modifications to appear as an update or exploiting vulnerabilities that allow activities of the malicious application to run inside a system application.(Citation: CheckPoint Agent Smith)

---

### [ATTACK-PATTERN] Event Triggered Execution
- relevance: medium (matched: sms)

- **설명**:
Adversaries may establish persistence using system mechanisms that trigger execution based on specific events. Mobile operating systems have means to subscribe to events such as receiving an SMS message, device boot completion, or other device activities.

Adversaries may abuse these mechanisms as a means of maintaining persistent access to a victim via automatically and repeatedly executing malicious code. After gaining access to a victim’s system, adversaries may create or modify event triggers to point to malicious content that will be executed whenever the event trigger is invoked.

---

### [ATTACK-PATTERN] System Network Configuration Discovery
- relevance: medium (matched: sms)
- url: https://attack.mitre.org/techniques/T1422

- **설명**:
Adversaries may look for details about the network configuration and settings, such as IP and/or MAC addresses, of devices they access or through information discovery of remote systems.

Adversaries may use the information from [System Network Configuration Discovery](https://attack.mitre.org/techniques/T1422) during automated discovery to shape follow-on behaviors, including determining certain access within the target network and what actions to do next.

On Android, details of onboard network interfaces are accessible to apps through the `java.net.NetworkInterface` class.(Citation: NetworkInterface) Previously, the Android `TelephonyManager` class could be used to gather telephony-related device identifiers, information such as the IMSI, IMEI, and phone number. However, starting with Android 10, only preloaded, carrier, the default SMS, or device and profile owner applications can access the telephony-related device identifiers.(Citation: TelephonyManager)

On iOS, gathering network configuration information is not possible without root access.

Adversaries may use the information from [System Network Configuration Discovery](https://attack.mitre.org/techniques/T1422) during automated discovery to shape follow-on behaviors, including determining certain access within the target network and what actions to do next.

---

### [ATTACK-PATTERN] Prevent Application Removal
- relevance: high (matched: malicious app, malicious application)

- **설명**:
Adversaries may abuse the Android device administration API to prevent the user from uninstalling a target application. In earlier versions of Android, device administrator applications needed their administration capabilities explicitly deactivated by the user before the application could be uninstalled. This was later updated so the user could deactivate and uninstall the administrator application in one step.

Adversaries may also abuse the device accessibility APIs to prevent removal. This set of APIs allows the application to perform certain actions on behalf of the user and programmatically determine what is being shown on the screen. The malicious application could monitor the device screen for certain modals (e.g., the confirmation modal to uninstall an application) and inject screen input or a back button tap to close the modal. For example, Android's `performGlobalAction(int)` API could be utilized to prevent the user from removing the malicious application from the device after installation. If the user wants to uninstall the malicious application, two cases may occur, both preventing the user from removing the application.

* Case 1: If the integer argument passed to the API call is `2` or `GLOBAL_ACTION_HOME`, the malicious application may direct the user to the home screen from settings screen

* Case 2: If the integer argument passed to the API call is `1` or `GLOBAL_ACTION_BACK`, the malicious application may emulate the back press event

---

### [ATTACK-PATTERN] Phishing
- relevance: high (matched: qr code, quishing, phishing, smishing, spearphishing, credential, fake, social engineering, impersonat)

- **설명**:
Adversaries may send malicious content to users in order to gain access to their mobile devices. All forms of phishing are electronically delivered social engineering. Adversaries can conduct both non-targeted phishing, such as in mass malware spam campaigns, as well as more targeted phishing tailored for a specific individual, company, or industry, known as “spearphishing.” Phishing often involves social engineering techniques, such as posing as a trusted source, as well as evasion techniques, such as removing or manipulating emails or metadata/headers from compromised accounts being abused to send messages.

Mobile phishing may take various forms. For example, adversaries may send emails containing malicious attachments or links, typically to deliver and then execute malicious code on victim devices. Phishing may also be conducted via third-party services, like social media platforms. Adversaries may also impersonate executives of organizations to persuade victims into performing some action on their behalf. For example, adversaries will often use social engineering techniques in text messages to trick the victims into acting quickly, which leads to adversaries obtaining credentials and other information.

Mobile devices are a particularly attractive target for adversaries executing phishing campaigns.  Due to their smaller form factor than traditional desktop endpoints, users may not be able to notice minor differences between genuine and phishing websites. Further, mobile devices have additional sensors and radios that allow adversaries to execute phishing attempts over several different vectors, such as:

- SMS messages: Adversaries may send SMS messages (known as “smishing”) from compromised devices to potential targets to convince the target to, for example, install malware, navigate to a specific website, or enable certain insecure configurations on their device.
- Quick Response (QR) Codes: Adversaries may use QR codes (known as “quishing”) to redirect users to a phishing website. For example, an adversary could replace a legitimate public QR Code with one that leads to a different destination, such as a phishing website. A malicious QR code could also be delivered via other means, such as SMS or email. In the latter case, an adversary could utilize a malicious QR code in an email to pivot from the user’s desktop computer to their mobile device.
- Phone Calls: Adversaries may call victims (known as "vishing") to persuade them to perform an action, such as providing login credentials or navigating to malicious websites. Common vishing targets include employees, especially executives of organizations, and help desks. This may also be used as a technique to perform the initial access on a mobile device, but then pivot to a desktop computer by having the victims perform actions on a desktop computer. With the rise of artificial intelligence (AI), adversaries may also use AI to clone a person’s voice, resulting in deepfake vishing. The cloned voice provides familiarity to the victims, increasing the likelihood of successful malicious actions performed by the victims. Additionally, adversaries may leave voicemails, which may use a real person’s voice or an AI-generated voice; these scams would urgently ask victims into calling back to perform an action, e.g. sending money or providing sensitive information and credentials.

---

### [ATTACK-PATTERN] Lockscreen Bypass
- relevance: high (matched: spoof)

- **설명**:
An adversary with physical access to a mobile device may seek to bypass the device’s lockscreen. Several methods exist to accomplish this, including:

* Biometric spoofing: If biometric authentication is used, an adversary could attempt to spoof a mobile device’s biometric authentication mechanism. Both iOS and Android partly mitigate this attack by requiring the device’s passcode rather than biometrics to unlock the device after every device restart, and after a set or random amount of time.(Citation: SRLabs-Fingerprint)(Citation: TheSun-FaceID)
* Unlock code bypass: An adversary could attempt to brute-force or otherwise guess the lockscreen passcode (typically a PIN or password), including physically observing (“shoulder surfing”) the device owner’s use of the lockscreen passcode. Mobile OS vendors partly mitigate this by implementing incremental backoff timers after a set number of failed unlock attempts, as well as a configurable full device wipe after several failed unlock attempts.
* Vulnerability exploit: Techniques have been periodically demonstrated that exploit mobile devices to bypass the lockscreen. The vulnerabilities are generally patched by the device or OS vendor once disclosed.(Citation: Wired-AndroidBypass)(Citation: Kaspersky-iOSBypass)

---

### [ATTACK-PATTERN] Account Access Removal
- relevance: high (matched: credential)

- **설명**:
Adversaries may interrupt availability of system and network resources by inhibiting access to accounts utilized by legitimate users. Accounts may be deleted, locked, or manipulated (ex: credentials changed) to remove access to accounts.

---

### [ATTACK-PATTERN] Endpoint Denial of Service
- relevance: medium (matched: device administrator)

- **설명**:
Adversaries may perform Endpoint Denial of Service (DoS) attacks to degrade or block the availability of services to users.

On Android versions prior to 7, apps can abuse Device Administrator access to reset the device lock passcode, preventing the user from unlocking the device. After Android 7, only device or profile owners (e.g. MDMs) can reset the device’s passcode.(Citation: Android resetPassword)

On iOS devices, this technique does not work because mobile device management servers can only remove the screen lock passcode; they cannot set a new passcode. However, on jailbroken devices, malware has been discovered that can lock the user out of the device.(Citation: Xiao-KeyRaider)

---

### [ATTACK-PATTERN] Out of Band Data
- relevance: medium (matched: sms)

- **설명**:
Adversaries may communicate with compromised devices using out of band data streams. This could be done for a variety of reasons, including evading network traffic monitoring, as a backup method of command and control, or for data exfiltration if the device is not connected to any Internet-providing networks (i.e. cellular or Wi-Fi). Several out of band data streams exist, such as SMS messages, NFC, and Bluetooth.

On Android, applications can read push notifications to capture content from SMS messages, or other out of band data streams. This requires that the user manually grant notification access to the application via the settings menu. However, the application could launch an Intent to take the user directly there.

On iOS, there is no way to programmatically read push notifications.

---

### [ATTACK-PATTERN] Suppress Application Icon
- relevance: high (matched: credential, malicious app, malicious application)

- **설명**:
A malicious application could suppress its icon from being displayed to the user in the application launcher. This hides the fact that it is installed, and can make it more difficult for the user to uninstall the application. Hiding the application's icon programmatically does not require any special permissions.

This behavior has been seen in the BankBot/Spy Banker family of malware.(Citation: android-trojan-steals-paypal-2fa)(Citation: sunny-stolen-credentials)(Citation: bankbot-spybanker)

Beginning in Android 10, changes were introduced to inhibit malicious applications’ ability to hide their icon. If an app is a system app, requests no permissions, or does not have a launcher activity, the application’s icon will be fully hidden. Further, if the device is fully managed or the application is in a work profile, the icon will be fully hidden. Otherwise, a synthesized activity is shown, which is a launcher icon that represents the app’s details page in the system settings. If the user clicks the synthesized activity in the launcher, they are taken to the application’s details page in the system settings.(Citation: Android 10 Limitations to Hiding App Icons)(Citation: LauncherApps getActivityList)

---

### [ATTACK-PATTERN] Code Signing Policy Modification
- relevance: medium (matched: sms)
- url: https://attack.mitre.org/techniques/T1516

- **설명**:
Adversaries may modify code signing policies to enable execution of applications signed with unofficial or unknown keys. Code signing provides a level of authenticity on an app from a developer, guaranteeing that the program has not been tampered with and comes from an official source. Security controls can include enforcement mechanisms to ensure that only valid, signed code can be run on a device.

Mobile devices generally enable these security controls by default, such as preventing the installation of unknown applications on Android. Adversaries may modify these policies in a number of ways, including [Input Injection](https://attack.mitre.org/techniques/T1516) or malicious configuration profiles.

---

### [ATTACK-PATTERN] Domain Generation Algorithms
- relevance: high (matched: malicious app, malicious application)
- url: https://attack.mitre.org/techniques/T1637/001

- **설명**:
Adversaries may use [Domain Generation Algorithms](https://attack.mitre.org/techniques/T1637/001) (DGAs) to procedurally generate domain names for uses such as command and control communication   or malicious application distribution.(Citation: securelist rotexy 2018)

DGAs increase the difficulty for defenders to block, track, or take over the command and control channel, as there could potentially be thousands of domains that malware can check for instructions.

---

### [ATTACK-PATTERN] Drive-By Compromise
- relevance: high (matched: drive-by)
- url: https://attack.mitre.org/techniques/T1550/001

- **설명**:
Adversaries may gain access to a system through a user visiting a website over the normal course of browsing. With this technique, the user's web browser is typically targeted for exploitation, but adversaries may also use compromised websites for non-exploitation behavior such as acquiring an [Application Access Token](https://attack.mitre.org/techniques/T1550/001).

Multiple ways of delivering exploit code to a browser exist, including:

* A legitimate website is compromised where adversaries have injected some form of malicious code such as JavaScript, iFrames, and cross-site scripting.
* Malicious ads are paid for and served through legitimate ad providers.
* Built-in web application interfaces are leveraged for the insertion of any other kind of object that can be used to display web content or contain a script that executes on the visiting client (e.g. forum posts, comments, and other user controllable web content).

Often the website used by an adversary is one visited by a specific community, such as government, a particular industry, or region, where the goal is to compromise a specific user or set of users based on a shared interest. This kind of targeted attack is referred to a strategic web compromise or watering hole attack. There are several known examples of this occurring.(Citation: Lookout-StealthMango)

Typical drive-by compromise process:

1. A user visits a website that is used to host the adversary controlled content.
2. Scripts automatically execute, typically searching versions of the browser and plugins for a potentially vulnerable version.
    * The user may be required to assist in this process by enabling scripting or active website components and ignoring warning dialog boxes.
3. Upon finding a vulnerable version, exploit code is delivered to the browser.
4. If exploitation is successful, then it will give the adversary code execution on the user's system unless other protections are in place.
    * In some cases a second visit to the website after the initial scan is required before exploit code is delivered.

---

