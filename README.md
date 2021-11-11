# RegExGen
Goal is to generate RegEx which can match almost all strings in given list of n strings.
n can be upto 10k.

Sample input:
{
 www.abcdefgh.com,
 www.abcd789.com,
 www.abc123.com,
 hello i'm noise,
 i'm also noise,
 www.abcd.com
}

Output: www\\.abc.{1,5}\\.com

Sample input:
{
 www.abcdefgh.com,
 www.google.com,
 www.facebook.com,
 hello i'm noise,
 www.network.com
}
Output: www\\.{6,8}\\.com

