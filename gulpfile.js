const gulp = require("gulp");
const axios = require("axios");

gulp.task("createpr", async () => {
  // map input args to variables
  const tokenInput = process.argv[4];
  const sourceBranchInput = process.argv[6];
  const bitbucketRepoOwnerInput = process.argv[8];
  const bitbucketRepoSlugInput = process.argv[10];
  const defaultReviewersInput = process.argv[12];

  // create headers
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${tokenInput}`,
  };

  // parse default reviewers from string to object to array
  const defaultReviewersParsed = JSON.parse(defaultReviewersInput);
  const defaultReviewers = [];
  defaultReviewersParsed.forEach(item => defaultReviewers.push(item));

  // create json payload
  const postData = {
    title: 'Dependency arcimoto-lambda-global-dependencies release: update of submodule required',
    description: 'The `arcimoto-lambda-global-dependencies` repo was updated and this dependent repository needs to bring in those upstream changes.',
    source: {
      branch: {
        name: `${sourceBranchInput}`,
      },
    },
    destination: {
      branch: {
        name: "dev",
      },
    },
    close_source_branch: false,
    reviewers: defaultReviewers
  };
  const url = `https://api.bitbucket.org/2.0/repositories/${bitbucketRepoOwnerInput}/${bitbucketRepoSlugInput}/pullrequests`;

  // make request
  return axios.post(url, postData, { headers })
  .catch(function (error) {
    console.log(error);
  });
})