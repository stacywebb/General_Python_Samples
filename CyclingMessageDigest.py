#######################
#  Stacy E. Webb
#
#    01/20/2010
#
#######################



import hashlib

class CyclingMessageDigest(object):
    '''
Computes a sequence of message digests based on strings contained in the anchor array,
and indexed by a cycling counter passed into the digest generator.  The generator function
returns the cycleIndex's digest.  The cycle repeats at the cycleLength parameter.

The message digest algorithm and cycleLength is configured in the constructor.

This algorithm is used to store tokens associated the n'th login in a series of logins, with
credentials provided in the anchor array.

The token is used one-time (per cycle), kept on the server, and also transmitted to a browser
persistent cookie.  When presented back at the server, it authorizes the use of the login
credentials to rejoin the logged-in session.

The indexOfCycle function runs this algorithm in reverse (at computationally much higher expense)
and reports back if this token is generated anywhere in the series of valid tokens, or is indeed not
a member of the series.

If there is a violation, i.e. browser hands back an invalid token, the algorithm can determine
if the incorrect token belongs anywhere in the login cycle, else it's known to be tampered with.
Or if the token is found *earlier* than the current sequence, it is being replayed.
Or if the token is found *laster* in the current sequence, either indicates that an intruder
has broken the algorithm (or that the cycle has restarted).

The generate function is virtually instantaneous.
The index function (used only to analyze an intrusion) operates at a rate of about 1 second per
100,000 attempts.  Therefore large cycles (e.g. one million logins) are quite feasible.
    '''
    

    def __init__(self, cycleLength):
        self.cycleLength = cycleLength
        self.MESSAGE_DIGEST_ALGORITHM = hashlib.sha1
    
    def generateMessageDigest(self, anchors, cycleIndex):
        generator = self.MESSAGE_DIGEST_ALGORITHM()
        cycle = cycleIndex % self.cycleLength
        for anchor in anchors:
            generator.update(anchor)
        generator.update(str(cycle))
        return generator.hexdigest()
            
    def indexOfCycleWithinSeries(self, anchors, hexDigestValue):
        cycle = -1
        for cycle in range(0, self.cycleLength):
            nowDigest = self.generateMessageDigest(anchors, cycle)
            if nowDigest == hexDigestValue:
                result = cycle
        return result

        
        
    
        