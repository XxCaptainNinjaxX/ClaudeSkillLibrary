# Credits

**Forked from** [amgadelgamal/claude-council](https://github.com/amgadelgamal/claude-council)
(MIT): Claude-only subagent council, anonymized peer review with ranking, the main session
as chairman, per-member model choice, a quick mode, and the rule never to present seats as
other vendors.

Ideas adapted from these projects. No text or code was copied from them; licenses are as
each repo states (MIT unless noted).

- [bourbondog/amicus](https://github.com/bourbondog/amicus): per-claim agree/dispute votes,
  the peers-only Confirmed / Contested / Disputed / Singleton tiers, and a single
  DEFEND / AMEND / WITHDRAW rebuttal round
  (`skills/second-opinion/COUNCIL-DESIGN.md`).
- [0xNyk/council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence):
  update only when a specific flaw is named, and project overrides that rank below run
  flags.
- [TorpedoD/claude-council](https://github.com/TorpedoD/claude-council): keeping the
  strongest dissent separate from the consensus verdict, "breakers" that flip the
  recommendation, and stripping seat identity before review.
- [hex/claude-council](https://github.com/hex/claude-council): framing same-model
  agreement as a shared prior, not corroboration.
- [nyldn/claude-octopus](https://github.com/nyldn/claude-octopus): no simulated councils,
  and stopping below quorum instead of faking consensus.
- [am-will/codex-skills](https://github.com/am-will/codex-skills) (MIT in package.json):
  treating member output as untrusted input and varying answer order to reduce position
  bias.
- [karpathy/llm-council](https://github.com/karpathy/llm-council) (no license file; idea
  credited only): the original three-stage council of answers, anonymized ranking and a
  chairman.
