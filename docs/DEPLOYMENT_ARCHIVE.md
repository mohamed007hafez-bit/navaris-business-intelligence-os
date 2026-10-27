# NAVARIS deployment archive

## Project
- Repository: https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os
- Branch: main
- Public website target: https://mohamed007hafez-bit.github.io/navaris-business-intelligence-os/
- Primary source: [index.html](../index.html)
- Founder image source path used by the page: images/founder.jpg

## Deployment notes
- The website is a responsive, static, single-page profile with English/Arabic toggle.
- Tailwind CSS is loaded from the official CDN; custom CSS covers brand styling and layout.
- Lead calls-to-action open a pre-populated email to mohamed007hafez@gmail.com.
- Deployment workflow completed successfully on 2026-10-27. Run: https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os/actions/runs/40574708507
- The workflow prepared the public site artifact, configured Pages, uploaded the artifact, and completed the deployment job successfully. A direct visual/browser rendering check could not be completed by the available web fetcher, so final appearance should still be opened in a browser.

## Evidence and caveats
- Deployment commit: https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os/commit/bf44af144b68cf4735c7c24cb08e290ce781b635
- GitHub Actions deployment evidence (success): https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os/actions/runs/40574708507
- GitHub Actions history: https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os/actions
- Source history: https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os/commits/main
- Releases: https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os/releases
- The copy does not claim Halliburton employment, a current ISO certification, a guaranteed three-hour SLA, or a verified 25-year customs infrastructure. These claims require documentary confirmation before being advertised.
- The page describes a target operating model. Specific turnaround, availability, customs arrangements, and service commitments require written confirmation.
- Tailwind CDN is convenient for zero-capital static deployment, but a production build with compiled/minified CSS is preferable when a build pipeline is available.
- Deployment is not considered complete until the latest workflow is green and the public URL is checked after propagation.

## Change log
- Replaced the prior single-language page with bilingual EN/AR capability profile.
- Added service, sector, operating-loop, founder, and inquiry sections.
- Added accessible language-toggle labels, mobile-responsive layout, reduced-motion handling, and email CTA.
