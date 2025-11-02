from .CollectorBase import CollectorBase

class CollectPullRequests(CollectorBase):
    def execute(self, data: dict, metrics: dict, members) -> dict:
        pull_requests = data['pull_requests']
        total = 0
        merged = 0
        closed = 0
        not_merged_by_author = 0
        created_PRs_per_member = {member: 0 for member in members}
        merged_PRs_per_member = {member: 0 for member in members}
        
        for _, pull_request in pull_requests.items():
            # skip dependabot authored PRs entirely
            author = pull_request.get("author")
            if author == "dependabot":
                continue
        
            total += 1
        
            # increment created count only for known members (members dict already initialized)
            if author in created_PRs_per_member:
                created_PRs_per_member[author] += 1
            else:
                # optionally track unexpected authors separately or ignore
                # created_PRs_per_member[author] = 1
                pass
        
            # handle merges: merged_by may be None or external, ensure safe access and skip dependabot
            if pull_request.get('merged') != False:
                merged += 1
                merged_by = pull_request.get("merged_by")
                if merged_by != "dependabot":
                    if merged_by in merged_PRs_per_member:
                        merged_PRs_per_member[merged_by] += 1
                    else:
                        # optional: ignore or track unexpected merger
                        # merged_PRs_per_member[merged_by] = 1
                        pass
        
                if author != merged_by:
                    not_merged_by_author += 1
            elif pull_request.get('state') == 'CLOSED':
                closed += 1
                
        metrics['pull_requests'] = {
            'created' : created_PRs_per_member,
            'merged_per_member' : merged_PRs_per_member,
            'merged': merged,
            'not_merged_by_author': not_merged_by_author,
            'closed': closed,
            'total': total
        }
        return metrics
