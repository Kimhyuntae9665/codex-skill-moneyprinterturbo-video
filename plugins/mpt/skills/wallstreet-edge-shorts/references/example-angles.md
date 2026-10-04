# Dated Example Angles

These examples show how to turn public-document details into stories. They are dated research seeds as of 2026-09-05. Reopen every source and refresh the facts, market price, and valuation before use.

## NVIDIA and neoclouds: paid twice

**Good hook:** `네오클라우드 서버가 비면 누가 돈을 낼까요? 계약서에는 엔비디아가 나옵니다.`

Primary spine:

- NVIDIA's FY2027 Q2 call describes a take-or-pay commitment on part of a neocloud facility, a minimum revenue guarantee that supports financing, and participation in a portion of revenue above that floor: https://investor.nvidia.com/files/content_files/TRANSCRIPT_-NVIDIA-Corp-NVDA-US-Q2-2027-Earnings-Call-26-August-2026-5_00-PM-ET.pdf
- CoreWeave's public filing describes NVIDIA's obligation, subject to conditions, to purchase residual unsold capacity through April 13, 2032: https://www.sec.gov/Archives/edgar/data/1769628/000114036125036118/ny20053122x6_s4a.htm
- NVIDIA's January 2026 CoreWeave investment and the plan for more than 5 GW of AI factories by 2030 were filed here: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000044/crwv-20260123.htm

Safe conclusion: the disclosed structure can let NVIDIA earn on hardware and participate in some rental upside while helping a neocloud finance capacity.

Use as a labeled rumor lane, not as confirmed fact:

- `NVIDIA receives 50% of revenue or profit`—show `시장설 50%? · 비율 미공개` while explaining that the cited public statement confirms only a portion of revenue above the floor.
- `Every idle CoreWeave GPU runs Nemotron`—show `연결 추정` while explaining that the documents establish capacity obligations and separate model-development cloud arrangements, but not that exact routing.

Visual: data-center utilization bar → customer demand → NVIDIA backstop on the disclosed portion → lender confidence → revenue above floor returning to NVIDIA.

## NVIDIA: supply and capacity fortress

**Good hook:** `엔비디아가 예약한 건 GPU만이 아닙니다. 공급과 데이터센터 용량까지 2,790억 달러입니다.`

Primary spine:

- NVIDIA reported supply and capacity commitments increasing from $119 billion in the prior quarter to $279 billion as of July 26, 2026, while warning about land, power, shell, capital, demand timing, and supply-chain risk: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm

Potential analysis: the scale can secure future output and deployment capacity, but it also increases cancellation, inventory, timing, and counterparty risk. This is a capital-and-capacity story, not proof of future revenue.

Visual: foundry → memory/packaging → networking/systems → land/power/shell → AI cloud. Show the $279B commitment as reservations across the chain, not cash already spent or revenue already earned.

## NVIDIA: more than a GPU, without fake networking revenue

**Good hook:** `뉴스는 GPU만 보지만, 엔비디아가 파는 건 데이터센터 한 채의 구조입니다.`

Build the layers from separately sourced products and economics: accelerators, CPUs, NVLink or networking, systems, CUDA and model software, cloud distribution, and capacity financing.

Evidence boundary: NVIDIA reports `Compute & Networking` as a combined segment. Do not call the entire segment networking-only revenue or rank it against networking companies without a separately disclosed denominator.

Visual: reveal a physical AI factory layer by layer. Put disclosed segment revenue on the combined frame and keep sublayer contribution unlabeled unless separately disclosed.

## NVIDIA open-model R&D: a tempting but incomplete connection

NVIDIA's filing says cloud service agreements support research and development of open models such as Nemotron, Cosmos, and GR00T: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/R17.htm

This supports `NVIDIA pays for cloud capacity used in open-model R&D`. It does not alone support `the residual unsold CoreWeave capacity specifically runs Nemotron`. To tell the stronger story, find a contract, transcript, or technical announcement that connects the same capacity and workload.

## AWS and Anthropic: the customer became a silicon-scale project

**Good hook:** `AWS가 앤트로픽에 빌려준 건 서버 몇 대가 아닙니다. 거의 100만 개 Trainium 칩입니다.`

Primary spine:

- AWS's Trainium customer page quotes Anthropic saying almost one million Trainium2 chips are training and serving Claude: https://aws.amazon.com/ai/machine-learning/trainium/customers/
- AWS describes Project Rainier as nearly half a million Trainium2 chips in its infrastructure overview: https://aws.amazon.com/about-aws/global-infrastructure/innovation/

Resolve the apparently different numbers by checking dates and scope before scripting. One may refer to the named Rainier cluster and the other to broader direct and service usage.

Visual: map the dedicated data-center footprint → Trainium racks → Claude training and serving → AWS silicon utilization and customer lock-in. Pair with concentration and capex risk.

## AWS and OpenAI: no longer hypothetical

An old X angle might say `If OpenAI adopts Trainium`. As of February 27, 2026, OpenAI officially announced a commitment to consume approximately 2 GW of Trainium capacity through AWS and an expansion of the existing agreement by $100 billion over eight years: https://openai.com/index/amazon-partnership/

The Short should therefore ask about the economic effect of committed capacity, not speculate whether adoption will happen. Do not add Graviton unless a current primary source proves the relevant OpenAI workload uses it.

Visual: old hypothetical card crossed out → signed capacity figure → data-center power gauge → AWS custom-silicon utilization → capex and execution counterpoint.

## Capital allocation: behavior, not the headline amount

X leads about `buyback discipline` become useful only after verifying:

- quarterly cash spent on repurchases;
- average purchase price when disclosed or reproducibly calculated;
- diluted and period-end share-count change over a clearly labeled interval;
- stock-based compensation and issuance;
- management or director purchases through Form 4;
- competing uses of cash and leverage.

Visual: share price plus repurchase timing → treasury or retirement treatment → actual diluted share count → per-share consequence. Never equate authorization with execution or repurchase with cancellation.

## Additional story seeds

- A regulator opens a scoring or data standard and weakens a tollbooth business. Start from the X lead, then verify the final regulator action and issuer exposure.
- A customer filing reveals that one AI provider controls most of a landlord's revenue. Use the landlord's 10-Q to show concentration and take-or-pay economics.
- A used-equipment or product-price signal suggests demand. Verify it against backlog, revenue, utilization, lead time, and alternative explanations before calling it predictive.
- A company invests in suppliers or customers instead of maximizing buybacks. Map what access, distribution, or financing the investment buys, then quantify dilution and balance-sheet risk.
